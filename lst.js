
Map.addLayer(s1.median(),{bands: ['VV','VV','VV'],min: -20,max: 0,},'S1-image [median]');


var aoi = [add geometery]
// Zoom to regions of interest
Map.centerObject(aoi);

// import sentinel 1 and filter data series
var s1 =  ee.ImageCollection('COPERNICUS/S1_GRD')
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
    //.filter(ee.Filter.eq('instrumentMode', 'IW'))
    //.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
    .filterBounds(aoi)
    //.filterBounds(Map.getBounds(true))
    .filterDate('2020-04-01','2020-04-30')
    //.filter(ee.Filter.contains({leftField: ".geo", rightValue: aoi})) // Filter partial S1-Images of AOI
    .map(function(image){return image.clip(Map.getBounds(true))})
    .map(function(image){return image.addBands(image.select('VV').focal_median(parseFloat('50'),'circle','meters').rename('VV_smoothed'))}); // Smooth S1-Images

// Return the DN that maximizes interclass variance in S1-band (in the region).
var otsu = function(histogram) {
    var counts = ee.Array(ee.Dictionary(histogram).get('histogram'));
    var means = ee.Array(ee.Dictionary(histogram).get('bucketMeans'));
    var size = means.length().get([0]);
    var total = counts.reduce(ee.Reducer.sum(), [0]).get([0]);
    var sum = means.multiply(counts).reduce(ee.Reducer.sum(), [0]).get([0]);
    var mean = sum.divide(total);

    var indices = ee.List.sequence(1, size);

// Compute between sum of squares, where each mean partitions the data.
    var bss = indices.map(function(i) {
        var aCounts = counts.slice(0, 0, i);
        var aCount = aCounts.reduce(ee.Reducer.sum(), [0]).get([0]);
        var aMeans = means.slice(0, 0, i);
        var aMean = aMeans.multiply(aCounts)
            .reduce(ee.Reducer.sum(), [0]).get([0])
            .divide(aCount);
        var bCount = total.subtract(aCount);
        var bMean = sum.subtract(aCount.multiply(aMean)).divide(bCount);
        return aCount.multiply(aMean.subtract(mean).pow(2)).add(
            bCount.multiply(bMean.subtract(mean).pow(2)));
    });

// Return the mean value corresponding to the maximum BSS.
    return means.sort(bss).get([-1]);
};

// return image with water mask as additional band
var add_waterMask = function(image){
    // Compute histogram
    var histogram = image.select('VV').reduceRegion({
        reducer: ee.Reducer.histogram(255, 2)
            .combine('mean', null, true)
            .combine('variance', null, true),
        geometry: aoi,
        scale: 10,
        bestEffort: true
    });
    // Calculate threshold via function otsu (see before)
    var threshold = otsu(histogram.get('VV_histogram'));

    // get watermask
    var waterMask = image.select('VV_smoothed').lt(threshold).rename('waterMask').clip(aoi);
    waterMask = waterMask.updateMask(waterMask); //Remove all pixels equal to 0
    return image.addBands(waterMask);
};

s1 = s1.map(add_waterMask);

print(s1);

var water_max = s1.select('waterMask').max();
var water_max_poly = water_max.reduceToVectors({geometry: aoi,
    scale: 30})

// link to the code that computes the Landsat LST
var LandsatLST = require('users/sofiaermida/landsat_smw_lst:modules/Landsat_LST.js')



// select region of interest, date range, and landsat satellite
var geometry = aoi;
var satellite = 'L8';
var date_start = '2023-06-01';
var date_end = '2023-07-01';
var use_ndvi = true;

// get landsat collection with added variables: NDVI, FVC, TPW, EM, LST
var LandsatColl = LandsatLST.collection(satellite, date_start, date_end, geometry, use_ndvi)
print(LandsatColl)

// select the first feature
var exImage = LandsatColl.median();
var exImage = exImage.clip(geometry)
var exImage = exImage.clip(water_max_poly)
var palettes = require('users/gena/packages:palettes');
var LST_pal = palettes.kovesi.diverging_rainbow_bgymr_45_85_c67[7];
var cmap1 = ['blue', 'cyan', 'green', 'yellow', 'red'];
var cmap2 = ['F2F2F2','EFC2B3','ECB176','E9BD3A','E6E600','63C600','00A600'];

Map.centerObject(geometry)
// Map.addLayer(exImage.select('TPW'),{min:0.0, max:60.0, palette:cmap1},'TCWV')
// Map.addLayer(exImage.select('TPWpos'),{min:0.0, max:9.0, palette:cmap1},'TCWVpos')
// Map.addLayer(exImage.select('FVC'),{min:0.0, max:1.0, palette:cmap2}, 'FVC')
// Map.addLayer(exImage.select('EM'),{min:0.9, max:1.0, palette:cmap1}, 'Emissivity')
// Map.addLayer(exImage.select('B10'),{min:290, max:320, palette:cmap1}, 'TIR BT')
Map.addLayer(exImage.multiply(0.0000275).add(-0.2),{bands: ['SR_B4', 'SR_B3', 'SR_B2'], min:0, max:0.3}, 'RGB')
Map.addLayer(exImage.select('LST'),{min:295, max:305, palette:LST_pal}, 'LST')


function ColorBar(palette) {
    return ui.Thumbnail({
        image: ee.Image.pixelLonLat().select(0),
        params: {
            bbox: [0, 0, 1, 0.1],
            dimensions: '300x15',
            format: 'png',
            min: 0,
            max: 1,
            palette: palette,
        },
        style: {stretch: 'horizontal', margin: '0px 22px'},
    });
}
function makeLegend(lowLine, midLine, highLine,lowText, midText, highText, palette) {
    var  labelheader = ui.Label('LST Temp',{margin: '5px 17px', textAlign: 'center', stretch: 'horizontal', fontWeight: 'bold'});
    var labelLines = ui.Panel(
        [
            ui.Label(lowLine, {margin: '-4px 21px'}),
            ui.Label(midLine, {margin: '-4px 0px', textAlign: 'center', stretch: 'horizontal'}),
            ui.Label(highLine, {margin: '-4px 21px'})
        ],
        ui.Panel.Layout.flow('horizontal'));
    var labelPanel = ui.Panel(
        [
            ui.Label(lowText, {margin: '0px 14.5px'}),
            ui.Label(midText, {margin: '0px 0px', textAlign: 'center', stretch: 'horizontal'}),
            ui.Label(highText, {margin: '0px 1px'})
        ],
        ui.Panel.Layout.flow('horizontal'));
    return ui.Panel({
        widgets: [labelheader, ColorBar(palette), labelLines, labelPanel],
        style: {position:'bottom-center'}});
}
Map.add(makeLegend('|', '|', '|',  "River Temp", '+5 °C', '+ 10 °C', LST_pal));

// uncomment the code below to export a image band to your drive
/*
Export.image.toDrive({
  image: exImage.select('LST'),
  description: 'LST',
  scale: 30,
  region: geometry,
  fileFormat: 'GeoTIFF',
});
*/

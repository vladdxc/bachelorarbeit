sourcedirs = {'C:\Users\Vlad\Desktop\SatData\Multispectral\S2A_MSIL1C_20181001T143741_N0206_R096_T19LGH_20181001T163418.SAFE\GRANULE\L1C_T19LGH_A017110_20181001T143743\IMG_DATA',
              'C:\Users\Vlad\Desktop\SatData\Multispectral\S2A_MSIL1C_20190120T103341_N0207_R108_T30QYH_20190120T123745.SAFE\GRANULE\L1C_T30QYH_A018695_20190120T104403\IMG_DATA',
              'C:\Users\Vlad\Desktop\SatData\Multispectral\S2A_MSIL1C_20190216T102111_N0207_R065_T32TPT_20190216T122039.SAFE\GRANULE\L1C_T32TPT_A019081_20190216T102131\IMG_DATA',
              'C:\Users\Vlad\Desktop\SatData\Multispectral\S2A_MSIL1C_20190216T102111_N0207_R065_T32UPU_20190216T122039.SAFE\GRANULE\L1C_T32UPU_A019081_20190216T102131\IMG_DATA'};

R = georefcells();
dummy_info = {'s1a-ew-grd-hh-20190213t202833-20190213t202945-025916-02e2cc-001.tiff', 'blabla'};

for i = 1:numel(sourcedirs)
    directory = sourcedirs{i};
    bands = loadMultispectral(directory);
    image = resample10m(bands, 1);
    writeP(image, 120, R, dummy_info, i);
end

function patch = writePa(cell, bs, R, sourcefile, batchnumber)

					 
    rows = size(cell,1);
    cols = size(cell,2);
    k = 0;
    
    rowBlocks = rows/bs;
    colBlocks = cols/bs;
    
    for j = 1:rowBlocks 
        for i = 1:colBlocks    
            
            k = k + 1;
            patch = cell((j - 1)*bs + 1 : (j - 1)*bs + bs , (i - 1)*bs + 1 : (i - 1)*bs + bs, :);
            patchR = R; 
            patchR.RasterSize = R.RasterSize;
            info = geotiffinfo(sourcefile{1});
            filename = ['patch_' num2str(batchnumber) '_counter_' num2str(k) '.tif'];
            geotiffwrite(filename, patch, patchR,  ...
       'GeoKeyDirectoryTag', info.GeoTIFFTags.GeoKeyDirectoryTag);     
   
        end
    end
end
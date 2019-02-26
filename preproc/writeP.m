function patch = writeP(cell, bs, R, sourcefile, batchnumber)
%%WRITEP Splits data in 'cell' in patches and writes the contents to a .tif file
%	Input Arguments: cell - A m x n x c-array with multispectral or SAR data 
%					 bs - Length and width of a single patch
%					 R - A spatial refercing object generated georefcells(). Only needed for geotiffwrite to work well
%					 soucefile - File name of m x n x c-array. Needed for geoinformation
%					 batchnumber - Denotes the patch belonging to one m x n x c-array.
%					 
% 	Output: patch - A bs x bs x c-array of data written to the file in 'filename'.
					 
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
            patchR.RasterSize = [128 128];
            info = geotiffinfo(sourcefile{1});
            filename = ['patch_' num2str(batchnumber) '_counter_' num2str(k) '.tif'];
            geotiffwrite(filename, patch, patchR,  ...
       'GeoKeyDirectoryTag', info.GeoTIFFTags.GeoKeyDirectoryTag);     
   
        end
    end
end

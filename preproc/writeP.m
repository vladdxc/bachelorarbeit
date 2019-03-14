function patch = writeP(cell, bs, R, sourcefile, batchnumber, format, verbose)
%%WRITEP Splits data in 'cell' in patches and writes the contents to a .tif file
%	Input Arguments: cell - A m x n x c-array with multispectral or SAR data 
%					 bs - Length and width of a single patch
%					 R - A spatial refercing object generated georefcells(). Only needed for geotiffwrite to work well
%					 soucefile - File name of m x n x c-array. Needed for geoinformation
%					 batchnumber - Denotes the patch belonging to one m x n x c-array.
%					 format - String denoting the format to be written in.
%                             Valid formats are .tif and .mat
%                    verbose - Flag to display time elapsed for writing
%                              single patch. Valid values are 0, if nothing
%                              is to be displayed and 1 otherwise.
% 	Output: patch - A bs x bs x c-array of data written to the file in 'filename'.
					 
    rows = size(cell,1);
    cols = size(cell,2);
    k = 0;
    
    rowBlocks = rows/bs;
    colBlocks = cols/bs;
    
    for j = 1:rowBlocks 
        for i = 1:colBlocks    
            tic
            k = k + 1;
            patch = cell((j - 1)*bs + 1 : (j - 1)*bs + bs , (i - 1)*bs + 1 : (i - 1)*bs + bs, :);
            filename = ['patch_' num2str(batchnumber) '_counter_' num2str(k)];
            
            if format == 'tif'
                patchR = R; 
                patchR.RasterSize = [128 128];
                info = geotiffinfo(sourcefile{1});
                geotiffwrite([filename, '.tif'], patch, patchR,  ...
                'GeoKeyDirectoryTag', info.GeoTIFFTags.GeoKeyDirectoryTag);          
            elseif format == 'mat'
                save(filename, 'patch', '-v7.3')
            else
                error('Please give a valid file format! (tif or mat)')
            end 
            t = toc;
            
            if verbose == 1
                message = ['Patch ' num2str(k) 'written in ' num2str(t) ' seconds. \n'];
                fprintf(message)
            end
        end
    end
end

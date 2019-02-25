function image = MultiChannel(filenames, mode)
%MULTICHANNEL Computes intensity of SAR channels and returns a multidimensional array containing these. Also does normalization if necessary 
%   Input Arguments: filenames - A cell array of string with the filenames where the channel information
%                                is read from. Must contain exactly two entries.
%                    mode - A nu
%   Output: A mxnx2 array containing the intensities in both channels,
%   which are normalized to be zero mean and unit variance.

    [tmp1, ~] = geotiffread(filenames{1});
    [tmp2, ~] = geotiffread(filenames{2});
    
    [m n] = size(tmp1);
    image = zeros(m, n, 2);
    
    if mode == 1
        tmp1 = single(tmp1);
        tmp2 = single(tmp2);
        image(:,:, 1) = meanNorm(tmp1.*tmp1);
        image(:,:, 2) = meanNorm(tmp2.*tmp2);
    else
        image(:,:, 1) = tmp1;
        image(:,:, 2) = tmp2;
    end
    
    image = single(image);
end


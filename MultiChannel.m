function image = MultiChannel(filenames)
%MULTICHANNEL Computes intensity of VV and VH channels and returns a multidimensional array containing these. 
%   Input Arguments: A cell array of string with the filenames where the channel information
%   is read from. Must contain exactly two entries.
%
%   Output: A mxnx2 array containing the intensities in both channels,
%   which are normalized to be zero mean and unit variance.

    [tmp1, ~] = geotiffread(filenames{1});
    [tmp2, ~] = geotiffread(filenames{2});
    
    tmp1 = single(tmp1);
    tmp2 = single(tmp2);
    
    [m n] = size(tmp1);
    image = zeros(m, n, 2);
    
    image(:,:, 1) = meanNorm(tmp1.*tmp1);
    image(:,:, 2) = meanNorm(tmp2.*tmp2);
    
    image = single(image);
end


function image = resample10m(bands, mode)
%RESAMPLE10M Takes all bands, resamples them to 10m and normalizes data to zero mean and unit variance if wanted.
%   Input: bands - Cell array of size 13 x 1 with m x n arrays as contents.
%          mode - A number which should be 0 if no normalization is
%                 necessary and anything else if normalization is wanted. 
%   Output: A m_max x n_max x 13 array containing information in
%   all bands resampled to 10m resolution.

    m_max = max(cellfun('size', bands, 1));
    n_max = max(cellfun('size', bands, 2));
    s = [m_max n_max];
    
    image = zeros(m_max, n_max, numel(bands));
    
    for i = 1:numel(bands)
        if size(bands{i}) == s
            if mode == 0
                image(:,:,i) = bands{i};
            else 
                ret = single(bands{i});
                image(:,:,i) = single(meanNorm(ret));
            end
        else    
            ret = imresize(bands{i}, s, 'nearest');
            if mode == 0 
                image(:,:,i) = ret;
            else 
                image (:,:,i) = single(meanNorm(single(ret)));
            end
        end
    end    
    
    image = single(image);
end


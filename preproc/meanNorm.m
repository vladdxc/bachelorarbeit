function mat_norm = meanNorm(mat)
%MEANNORM A function that normalizes the data in 'mat' to zero mean and unit variance.
% Input Arguments: mat - A m x n array of data.
% Output: mat_norm - A m x n array of data with zero mean and unit variance.
    
    mu = 0;
    sigma = 0;

    mu = mean(mat(:));
    sigma = std(mat(:));
    mat_norm = (mat - mu)./sigma; 

end
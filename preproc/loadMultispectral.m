function Seq = loadMultispectral(imgPath)
    %imgPath = 'path\to\images\folder\';
    images  = dir([imgPath]);
    N = length(images);

    % check images
    if( ~exist(imgPath, 'dir') || N<1 )
        display('Directory not found or no matching images found.');
    end

    % preallocate cell
    Seq = cell(N,1);
    k = 1;

    for idx = 1:N
        if images(idx).isdir == 0
            Seq{k} = imread([images(idx).name]);
            k = k + 1;
        end
    end
    
    Seq = Seq(1:13);
end
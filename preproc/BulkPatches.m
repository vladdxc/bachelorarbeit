addpath(genpath('C:\Users\Vlad\Desktop\SatData'))
addpath(genpath('C:\Users\Vlad\Desktop\bachelorarbeit\preproc'))
%%
sourcefiles = {{'s1a-ew-grd-hv-20190213t202833-20190213t202945-025916-02e2cc-002.tiff','s1a-ew-grd-hh-20190213t202833-20190213t202945-025916-02e2cc-001.tiff'}
                {'s1a-iw-grd-vh-20190206t093908-20190206t093933-025807-02ded0-002.tiff','s1a-iw-grd-vv-20190206t093908-20190206t093933-025807-02ded0-001.tiff'}
                {'s1a-iw-grd-vh-20190213t170653-20190213t170718-025914-02e2b7-002.tiff','s1a-iw-grd-vv-20190213t170653-20190213t170718-025914-02e2b7-001.tiff'}
                {'s1a-iw-grd-vh-20190213t170718-20190213t170743-025914-02e2b7-002.tiff','s1a-iw-grd-vv-20190213t170718-20190213t170743-025914-02e2b7-001.tiff'}
                {'s1a-iw-grd-vh-20190215t182209-20190215t182234-025944-02e3c6-002.tiff','s1a-iw-grd-vv-20190215t182209-20190215t182234-025944-02e3c6-001.tiff'}
                {'s1a-iw-grd-vh-20190215t182234-20190215t182259-025944-02e3c6-002.tiff','s1a-iw-grd-vv-20190215t182234-20190215t182259-025944-02e3c6-001.tiff'}
                {'s1b-iw-grd-vh-20190214t041219-20190214t041244-014937-01be38-002.tiff','s1b-iw-grd-vv-20190214t041219-20190214t041244-014937-01be38-001.tiff'}
                {'s1b-iw-grd-vh-20190214t041244-20190214t041309-014937-01be38-002.tiff','s1b-iw-grd-vv-20190214t041244-20190214t041309-014937-01be38-001.tiff'}};
R = georefcells();
% image = cell(numel(sourcefiles), 1);

%for i = 7:numel(sourcefiles)
    filenames = sourcefiles{8};
    image = MultiChannel(filenames, 0);
    writeP(image, 128, R, filenames, 8, 'mat', 1);
%end



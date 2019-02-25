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
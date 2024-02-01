function real = pixel_coo_to_real(pixel) 
    fx = 1400;fy = 1400;
%     u0 = 932;
    u0 = 1920/2;
%     v0 = 526;
    v0 = 1080/2;
s = 0;K = [fx s u0 ; 0 fy v0 ; 0 0 1 ];

    coo = inv(K)*[pixel(1);pixel(2);1;]*696;
    coo =[coo;1];
    zc = 696    ;
    R_T_W = [-1 0 0 0;
                 0 1 0 0;
                 0 0 -1 zc;
                 0 0 0 1];
    final = R_T_W*coo;
    real=[final(1) final(2)];
end

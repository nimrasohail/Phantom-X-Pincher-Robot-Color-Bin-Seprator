function [world_coords] = cam_to_world_coords(cam_coords) 
    cam_coords % for checking
    % defining camera parameters
    fx = 1400;fy = 1400;
    u0 = 932;
%     u0 = 1920/2;
     v0 = 526;
%     v0 = 1080/2;
    s = 0;

    Intrinsic_trans = [fx s u0 ; 0 fy v0 ; 0 0 1];
    % array to store (x,y) of world coords
    world_coords = zeros(2,length(cam_coords));
    Z_c = 660;
    % looping over cube (x,y) to transform the coordinates to real world
    for k = 1:length(cam_coords)
       pts_transformed_in_cam = inv(Intrinsic_trans)*[cam_coords{k}(1);cam_coords{k}(2);1]*660;
       pts_transformed_in_cam =[pts_transformed_in_cam;1];
       zc = 660;
       R_T_W = [1 0 0 0;
        0 -1 0 0;
        0 0 -1 zc;
        0 0 0 1];
       final_ = R_T_W*pts_transformed_in_cam;
       world_coords(1,k) = final_(1);
       world_coords(2,k) = final_(2);
   end

end

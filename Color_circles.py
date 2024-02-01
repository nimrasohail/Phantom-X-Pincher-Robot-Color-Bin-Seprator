function location =  colour_object_detection(The_color)
    %% Create all objects to be used in this file
    % Make Pipeline object to manage streaming
    pipe = realsense.pipeline();
    % Make Colorizer object to prettify depth output
    colorizer = realsense.colorizer();
    % Create a config object to specify configuration of pipeline
    cfg = realsense.config();

    
    %% Set configuration and start streaming with configuration
    % Stream options are in stream.m
%     streamType = realsense.stream('depth');
    % Format options are in format.m
%     formatType = realsense.format('Distance');
    % Enable default depth
%     cfg.enable_stream(streamType,formatType);
    % Enable color stream
    streamType = realsense.stream('color');
    formatType = realsense.format('rgb8');
    cfg.enable_stream(streamType,formatType);
    
    % Start streaming on an arbitrary camera with chosen settings
    profile = pipe.start();

    %% Acquire and Set device parameters 
    % Get streaming device's name
    dev = profile.get_device(); %colour sensor + IR sensor    
    name = dev.get_info(realsense.camera_info.name);

    % Access Depth Sensor
    depth_sensor = dev.first('depth_sensor');

    % Access RGB Sensor
    rgb_sensor = dev.first('roi_sensor');
    
    % Find the mapping from 1 depth unit to meters, i.e. 1 depth unit =
    % depth_scaling meters.
    depth_scaling = depth_sensor.get_depth_scale();

    % Set the control parameters for the depth sensor
    % See the option.m file for different settable options that are visible
    % to you in the viewer. 
    optionType = realsense.option('visual_preset');
    % Set parameters to the midrange preset. See for options:
    % https://intelrealsense.github.io/librealsense/doxygen/rs__option_8h.html#a07402b9eb861d1defe57dbab8befa3ad
    depth_sensor.set_option(optionType,9);

    % Set autoexposure for RGB sensor
    optionType = realsense.option('enable_auto_exposure');
    rgb_sensor.set_option(optionType,1);
    optionType = realsense.option('enable_auto_white_balance');
    rgb_sensor.set_option(optionType,1);    
    
    %% Align the color frame to the depth frame and then get the frames
    % Get frames. We discard the first couple to allow
    % the camera time to settle
    for i = 1:5
        fs = pipe.wait_for_frames();
    end
    
%     % Alignment
%     align_to_depth = realsense.align(realsense.stream.depth);
%     fs = align_to_depth.process(fs); 

    % Stop streaming
    pipe.stop();


    %% Color Post-processing
    % Select color frame
    color = fs.get_color_frame(); %fs is the video pipeline

   
    %% Display RGB frame
    % Get actual data and convert into a format imshow can use
    % (Color data arrives as [R, G, B, R, G, B, ...] vector)fs
    data2 = color.get_data();
    myMatrix6 = color.get_data();
    save('data3.mat', 'myMatrix6');
    fprintf('The width is %d \n', color.get_width())
    im = permute(reshape(data2',[3,color.get_width(),color.get_height()]),[3 2 1]);
    img = im;
     min = [102 0 0];
    max = [255.0000  145  145];
%     figure; imshow(im);title("Original Image"); figure;
    % Threshold the image to extract the red regions
    red_mask = (img(:,:,1) >= min(1)) & (img(:,:,1) <= max(1)) & (img(:,:,2) >= min(2)) & (img(:,:,2) <= max(2)) & (img(:,:,3) <= max(3)) & (img(:,:,3) >= min(3));
%     figure; imshow(red_mask); title("Post Thresholding"); figure;
    % Clean up the mask using morphological operations
    se = strel('square', 6);
    red_mask = imclose(imopen(red_mask, se), se);
%     figure; imshow(red_mask); title("Post Morphological Operations"); figure;
    % figure;
    % imshow(red_mask)
    % figure;
      % Find connected components in the mask
    cc = bwconncomp(red_mask);
    
    % Extract the location of the red cubes as a list of centroids
    stats = regionprops(cc, 'Centroid');
    red_cubes = cat(1, stats.Centroid);
    true_red = [];
    if size(red_cubes) ~= 0
        for i = 1:size(red_cubes)
            if (~(810 <= red_cubes(i,1) && red_cubes(i,1) <= 1137 && 282 <= red_cubes(i,2) && red_cubes(i,2) <= 611)) && (~(1158 <= red_cubes(i,1) && red_cubes(i,1) <= 1400 && 164 <= red_cubes(i,2) && red_cubes(i,2) <= 400)) && 332<= red_cubes(i,1) && red_cubes(i,1) <= 1608
                true_red = [true_red; red_cubes(i,1) red_cubes(i,2)];
            end
        end
    end
    
    disp(red_cubes);
    disp(size(red_cubes));
    % Display the image with the red cubes marked

    imshow(img);

    hold on;
    if size(true_red) ~= 0
        plot(true_red(:,1), true_red(:,2), 'ro', 'MarkerSize', 10, 'LineWidth', 2);
        hold on;
    end
    %blue
    min = [0 0 140];
    max = [110.0000  125  255.0000];
    blue_mask = (img(:,:,1) >= min(1)) & (img(:,:,1) <= max(1)) & (img(:,:,2) >= min(2)) & (img(:,:,2) <= max(2)) & (img(:,:,3) <= max(3)) & (img(:,:,3) >= min(3));
%     figure; imshow(blue_mask); figure;
      
    se = strel('square', 5);
    blue_mask = imclose(imopen(blue_mask, se), se);
    
      
    cc = bwconncomp(blue_mask);
    
     
    stats = regionprops(cc, 'Centroid');
    blue_cubes = cat(1, stats.Centroid);
    true_blue = [];
    if size(blue_cubes) ~= 0
        for i = 1:size(blue_cubes)
            if (~(810 <= blue_cubes(i,1) && blue_cubes(i,1) <= 1137 && 282 <= blue_cubes(i,2) && blue_cubes(i,2) <= 611)) && (~(1044 <= blue_cubes(i,1) && blue_cubes(i,1) <= 1224 && 81 <= blue_cubes(i,2) && blue_cubes(i,2) <= 389)) && 332<= blue_cubes(i,1) && blue_cubes(i,1) <= 1608

                true_blue = [true_blue; blue_cubes(i,1) blue_cubes(i,2)];
            end
        end
    end
    disp(blue_cubes);
    disp(size(blue_cubes));
    % Display the image with the red cubes marked
    if size(true_blue) ~= 0
        plot(true_blue(:,1), true_blue(:,2), 'bo', 'MarkerSize', 10, 'LineWidth', 2);
        hold on;
    end
    % yellow
    min = [153 153 0];
    max = [255   255   150];
    yellow_mask = (img(:,:,1) >= min(1)) & (img(:,:,1) <= max(1)) & (img(:,:,2) >= min(2)) & (img(:,:,2) <= max(2)) & (img(:,:,3) <= max(3)) & (img(:,:,3) >= min(3));
    
      
    se = strel('square', 6);
    yellow_mask = imclose(imopen(yellow_mask, se), se);
    
      
    cc = bwconncomp(yellow_mask);
    
     
    stats = regionprops(cc, 'Centroid');
    yellow_cubes = cat(1, stats.Centroid);
    true_yellow = [];
    if size(yellow_cubes) ~= 0
        for i = 1:size(yellow_cubes)
            if (~(810 <= yellow_cubes(i,1) && yellow_cubes(i,1) <= 1137 && 282 <= yellow_cubes(i,2) && yellow_cubes(i,2) <= 611)) && (~(1044 <= yellow_cubes(i,1) && yellow_cubes(i,1) <= 1224 && 81 <= yellow_cubes(i,2) && yellow_cubes(i,2) <= 389)) && 332<= yellow_cubes(i,1) && yellow_cubes(i,1) <= 1608
                true_yellow = [true_yellow; yellow_cubes(i,1) yellow_cubes(i,2)];
            end
        end
    end
    disp(yellow_cubes);
    disp(size(yellow_cubes));
    % Display the image with the red cubes marked
    if size(true_yellow) ~= 0
        plot(true_yellow(:,1), true_yellow(:,2), 'yo', 'MarkerSize', 10, 'LineWidth', 2);
        hold on;
    end
    % green
    min = [0   102   102];
    max = [110.0000  200.0000  145];
    green_mask = (img(:,:,1) >= min(1)) & (img(:,:,1) <= max(1)) & (img(:,:,2) >= min(2)) & (img(:,:,2) <= max(2)) & (img(:,:,3) <= max(3)) & (img(:,:,3) >= min(3));
    % imshow(green_mask)
    % figure
      
    se = strel('square', 17);
    green_mask = imclose(imopen(green_mask, se), se);
    
      
    cc = bwconncomp(green_mask);
    
     
    stats = regionprops(cc, 'Centroid');
    green_cubes = cat(1, stats.Centroid);
    true_green = [];
    if size(green_cubes) ~= 0
        for i = 1:size(green_cubes)
            if (~(810 <= green_cubes(i,1) && green_cubes(i,1) <= 1137 && 282 <= green_cubes(i,2) && green_cubes(i,2) <= 611)) && (~(1044 <= green_cubes(i,1) && green_cubes(i,1) <= 1224 && 81 <= green_cubes(i,2) && green_cubes(i,2) <= 389)) && 332<= green_cubes(i,1) && green_cubes(i,1) <= 1608

                true_green = [true_green; green_cubes(i,1) green_cubes(i,2)];
            end
        end
    end

    disp(green_cubes);
    disp(size(green_cubes));

    if size(true_green) ~= 0
        plot(true_green(:,1), true_green(:,2), 'go', 'MarkerSize', 10, 'LineWidth', 2);
        hold on;
    end

%     if size(true_green) ~= 0
%         plot(true_green(:,1), true_green(:,2), 'go', 'MarkerSize', 10, 'LineWidth', 2);
%         hold on;
%     end

    
if The_color == 1     %if the object is of color red
    disp('The object is of color Red')
    location = true_red;
elseif The_color == 2 %if the object is of color blue
    disp('The object is of color Blue')
    location = true_blue;
elseif The_color == 3 %if the object is of color green
    disp('The object is of color Green')
    location = true_green;
elseif The_color == 4 %if the object is of color
    disp('The object is of color Yellow')
    location = true_yellow;
end
    
end

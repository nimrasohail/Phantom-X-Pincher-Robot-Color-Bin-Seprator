function pick_and_place_cube(pick_coords,place_coords)
    current_state = 0;
    % removing offset in the z-coord
    pick_coords(3) = pick_coords(3) + 2;
    place_coords(3) = place_coords(3) + 2;
    
    height_of_block = 2.8; % cm

   
while 1
    % pick phenomenon
    current_state
    if current_state == 0
        arb = Arbotix('port', 'COM12', 'nservos', 5);
        arb.setpos([0,0,-pi/4,-pi/2,0],[25,25,25,25,25]);
        pause(5);
        error_ = find_error([0,0,0,0,0],[arb.getpos]);
        if error_ == false
            current_state = 1;
        else
            current_state = 0;
        end
   current_state
   elseif current_state == 1
        pick_coords(3) = pick_coords(3) + 2*height_of_block;
        coords_1 = findOptimalsoln(pick_coords(1),pick_coords(2),pick_coords(3),pick_coords(4),pick_coords(5));

        current_state = 2;
    current_state
    elseif current_state == 2
        setPosition(coords_1,0);
        pause(5);
        arb = Arbotix('port', 'COM12', 'nservos', 5);
        curr_pos = arb.getpos;
        error_1 = find_error([coords_1,0],[curr_pos]);
        if error_1 == false
            current_state = 3;
        else
            current_state = 2;
        end
    current_state
    elseif current_state == 3
        pick_coords(3) = pick_coords(3) - 4*height_of_block;
        coords_2 = findOptimalsoln(pick_coords(1),pick_coords(2),pick_coords(3),pick_coords(4),pick_coords(5));
       
        setPosition(coords_2,0);
        pause(5);
        arb = Arbotix('port', 'COM12', 'nservos', 5);
        curr_pos = arb.getpos();
        error_1 = find_error([coords_2,0],[curr_pos]);
        
        if error_1 == false
            current_state = 4;
        else
            current_state = 3;
        end
    current_state
    elseif current_state == 4
        setPosition(coords_2,1.2);
        pause(5);
        arb = Arbotix('port', 'COM12', 'nservos', 5);
         if arb.getpos(5) > 0.9
            current_state = 5;
        else
            current_state = 4;
         end
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
    % place phenomenon
    current_state
     elseif current_state == 5
        place_coords(3) = place_coords(3) + 2*height_of_block;
        coords_3 = findOptimalsoln(place_coords(1),place_coords(2),place_coords(3),place_coords(4),place_coords(5));
        current_state = 6;
    current_state
    elseif current_state == 6
        setPosition(coords_3,1.2);
        pause(5);
        arb = Arbotix('port', 'COM12', 'nservos', 5);
        curr_pos_ = arb.getpos
        error_3 = find_error([coords_3,1.1556],[curr_pos_]);
        if error_3 == false
            current_state = 7;
        else
            current_state = 6;
        end
    current_state
    elseif current_state == 7
        place_coords(3) = place_coords(3) - 4*height_of_block - 1;
        coords_4_ = findOptimalsoln(place_coords(1),place_coords(2),place_coords(3),place_coords(4),place_coords(5));
       
        setPosition(coords_4_,1.2);
        pause(5);
        arb = Arbotix('port', 'COM12', 'nservos', 5);
        curr_pos = arb.getpos();
        error_4 = find_error([coords_4_,1.2],[curr_pos]);
        
        if error_4 == false
            current_state = 8;
        else
            current_state = 7;
        end
    current_state
    elseif current_state == 8
        setPosition(coords_4_,0.8);
        pause(5);
        arb = Arbotix('port', 'COM12', 'nservos', 5);
        current_state = 0;
    end
end
end

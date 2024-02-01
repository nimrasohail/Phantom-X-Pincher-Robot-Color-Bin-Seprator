function solutions = findJointAngles_O(x,y,z,phi) 
theta_1_1 = atan2(y,x); %%
theta_1_2 = atan2(y,x)+pi;

d_1 = 142;
a_4 = 80;
a_3 = 104;
a_2 = 104;

r = sqrt(x^2 + y^2);
s = z - d_1;
x_new= r - a_4*cos(phi);
y_new= s - a_4*sin(phi);

alpha = acos((-(x_new^2 + y_new^2) + a_2^2 + a_3^2)/(2*a_2*a_3));
temp = (a_2^2 + y_new^2 + x_new^2 - a_3^2)/ (2 * a_2 * sqrt(y_new^2 + x_new^2));
beta = (atan2(sqrt(1 - temp^2),temp));
gamma = atan2(y_new,x_new);


theta_2_1 = (gamma - beta);
theta_2_2 = gamma + beta ;

theta_3_1 = pi - alpha;
theta_3_2 = - pi + alpha;

theta_4_1 = phi - theta_3_1 - theta_2_1;
theta_4_2 = phi - theta_3_2 - theta_2_2;

solutions = [theta_1_1 theta_2_1 theta_3_1 theta_4_1;

theta_1_1 theta_2_2 theta_3_2 theta_4_2;

theta_1_2 pi-theta_2_1  -theta_3_1 -theta_4_1;

theta_1_2 pi-theta_2_2 -theta_3_2 -theta_4_2];

for x = 1:4
    for y = 1:4
        verify = error1(solutions(x,y));
        if ((verify > 150*(pi/180) && verify< pi) |  (verify < -150*(pi/180) && verify > -pi))
            disp("Angles limits are outside 150 degrees or -150 degrees")
            disp([x,y])
        end
        solutions(x,y) = verify;
    end
end 



% solutions = [theta_1_1-pi/2 theta_2_1+pi/2 theta_3_1 theta_4_1;
% 
% theta_1_1-pi/2 theta_2_2+pi/2 theta_3_2 theta_4_2;
% 
% theta_1_2-pi/2 pi-theta_2_1+pi/2  -theta_3_1 -theta_4_1;
% 
% theta_1_2-pi/2 pi-theta_2_2+pi/2 -theta_3_2 -theta_4_2];
%display(solutions*180/pi);

end

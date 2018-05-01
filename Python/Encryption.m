I=imread('lena.png');
I_imag = double(I);
I_imag = complex(I_imag);
seed = 0.571;
seed2 = 0.572;
seed3 = 0.573;
for x = 1:512
    for y = 1:512
        seed = r*seed*(1-seed);
        seed2 = r*seed2*(1-seed2);
        seed3 = r*seed3*(1-seed3);
        I_imag(x,y) = I_imag(x,y) * complex ( sin(360 * seed), -cos(360 * seed2) );
    end
end
imshow(uint8(I_imag));

F=fft2(double(I_imag));
seed = 0.571;
seed2 = 0.572;
seed3 = 0.573;
r = 3.88;
x=0;
y=0;
z=0;

maskimg = randn(512,512);
maskimg = complex(maskimg);

maskimg = F;

for x = 1:512
    for y = 1:512
        seed = r*seed*(1-seed);
        seed2 = r*seed2*(1-seed2);
        seed3 = r*seed3*(1-seed3);
        maskimg(x,y) = maskimg(x,y) * complex ( sin(360 * seed), -cos(360 * seed2) );
    end
end
seed = 0.571;
seed2 = 0.572;
seed3 = 0.573;
for x = 1:512
    for y = 1:512
        seed = r*seed*(1-seed);
        seed2 = r*seed2*(1-seed2);
        seed3 = r*seed3*(1-seed3);
        maskimg(x,y) = maskimg(x,y) / complex ( sin(360 * seed), -cos(360 * seed2) );
    end
end


I_imag = ifft2(maskimg);
seed = 0.571;
seed2 = 0.572;
seed3 = 0.573;
for x = 1:512
    for y = 1:512
        seed = r*seed*(1-seed);
        seed2 = r*seed2*(1-seed2);
        seed3 = r*seed3*(1-seed3);
        I_imag(x,y) = I_imag(x,y) / complex ( sin(360 * seed), -cos(360 * seed2) );
    end
end
%{
for x = 1:512
    for y = 1:512
        I(x,y) = abs(I(x,y));
    end
end
%}
I = uint8(I);



imshow(uint8(I));



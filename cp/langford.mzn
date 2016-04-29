%
% Team: Waldemar Cruz, Samir Dahmani
%

include "globals.mzn";
%Modify the following two variables to change the parameters
%k <- the number of occurences of a digit; digit <- the range of digits from 1 to digits
int: digits = 9;
int: k = 3;
int: n = digits * k;

array[1..n] of var 1..n: a; %Array for Series

%Each occurence of a digit must occupy one space and only that particular digit may occupy that position (exclusivity)
constraint alldifferent([a[i] | i in 1..n]);

%For a particular digit d, it must be the case that the next occurence of the digit is exactly the d + 1 positions away; In other words, there must be a gap between occurences of a digit equal to its value.
constraint forall(i in 0..digits-1, j in 1..k-1)(
  a[i*k+j] = a[i*k+j+1] + (i+2)
);

solve satisfy;

output [ show([ceil(j / k) |i,j in 1..n where a[j] = i])];
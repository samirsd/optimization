%
% Team: Waldemar Cruz, Samir Dahmani
%

include "alldifferent.mzn";
int: N = 7; %Set Matrix Size
int: digs = ceil(log(10.0,int2float(N))); % digits for output
set of int: MatrixRange = 0..N-1;


array[0..N-1,0..N-1] of var MatrixRange: matrix;


%Quasigroup rule over * ((a*(b*a))=((b*a)*a))
constraint forall (a, b in MatrixRange)(
  matrix[a,matrix[b,a]] = matrix[matrix[b,a],a] );

%Idempotent Rule
constraint forall (i in MatrixRange)(
  matrix[i,i] = i );

% All different in rows
constraint forall (i in MatrixRange) (
  alldifferent( [ matrix[i,j] | j in MatrixRange ]) );

% All different in columns.
constraint forall (j in MatrixRange) (
  alldifferent( [ matrix[i,j] | i in MatrixRange ]) );


solve satisfy;

output [ show_int(digs,matrix[i,j]) ++ " " ++
if j == N-1 /\ i != N-1 then
if i mod N-1 == 0 then "\n" else "\n" endif
else "" endif
| i,j in MatrixRange ] ++ ["\n"];
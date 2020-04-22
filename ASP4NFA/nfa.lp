#include "facts.lp".

x(P, N) :- prefix(P), q(N), not not_x(P, N).
not_x(P, N) :- prefix(P), q(N), not x(P, N).
has_state(P) :- prefix(P), q(N), x(P, N).
:- prefix(P), not has_state(P).
final(N) :- q(N), not not_final(N).
not_final(N) :- q(N), not final(N).
delta(Q, A, R) :- q(Q), symbol(A), q(R), not not_delta(Q, A, R).
not_delta(Q, A, R) :- q(Q), symbol(A), q(R), not delta(Q, A, R).
:- not x(lambda, 0).
:- x(lambda, N), q(N), N != 0.
:- q(N), x(W, N), final(N), negative(W).
:- positive(W), {final(N) : q(N), x(W, N)} = 0.
x(V, R) :- q(Q), q(R), join(U, A, V), x(U, Q), delta(Q, A, R).
:- join(U, A, V), q(N), x(V, N), {delta(J, A, N) : q(J), x(U, J)} = 0.

#show final/1.  #show delta/3.

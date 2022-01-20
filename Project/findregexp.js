const {Alternation, CharClass, Concatenation, Repetition, Literal} = require('./ast');

/**
 * Implements Brzozowski's algebraic method to convert a DFA into a regular
 * expression pattern.
 * http://cs.stackexchange.com/questions/2016/how-to-convert-finite-automata-to-regular-expressions#2392
 *
 * @param {State} root - the initial state of the DFA
 * @param {string} flags - The flags to add to the regex.
 * @return {String} - the converted regular expression pattern
 */
function toRegex(root, flags) {
  let states = Array.from(root.visit());

  // Setup the system of equations A and B from Arden's Lemma.
  // A represents a state transition table for the given DFA.
  // B is a vector of accepting states in the DFA, marked as epsilons.
  let A = [];
  let B = [];

  for (let i = 0; i < states.length; i++) {
    let a = states[i];
    if (a.accepting) {
      B[i] = new Literal('');
    }

    A[i] = [];
    for (let [t, s] of a.transitions) {
      let j = states.indexOf(s);
      A[i][j] = A[i][j] ? union(A[i][j], new Literal(t)) : new Literal(t);
    }
  }

  // Solve the of equations
  for (let n = states.length - 1; n >= 0; n--) {
    if (A[n][n] != null) {
      B[n] = concat(star(A[n][n]), B[n]);
      for (let j = 0; j < n; j++) {
        A[n][j] = concat(star(A[n][n]), A[n][j]);
      }
    }

    for (let i = 0; i < n; i++) {
      if (A[i][n] != null) {
        B[i] = union(B[i], concat(A[i][n], B[n]));
        for (let j = 0; j < n; j++) {
          A[i][j] = union(A[i][j], concat(A[i][n], A[n][j]));
        }
      }
    }
  }

  return B[0].toString(flags);
}

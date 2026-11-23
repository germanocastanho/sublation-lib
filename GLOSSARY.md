# Glossary

Canonical terms for the `sublation` domain. Devoid of implementation details.

## Terms

**mu**: degree of evidence in favor of a proposition. Ranges over `[0.0, 1.0]`. Independent of `lam`.

**lam**: degree of evidence against a proposition. Ranges over `[0.0, 1.0]`. Independent of `mu`.

**TruthValue**: a pair `(mu, lam)` representing the evidential state of a proposition. The four corners are true `(1, 0)`, false `(0, 1)`, contradictory `(1, 1)`, and indeterminate `(0, 0)`.

**Thesis**: a dialectical position asserting a proposition as posited. Wraps a `TruthValue`.

**Antithesis**: a dialectical position asserting the negation of a thesis. Wraps a `TruthValue`.

**Synthesis**: the interaction between a `Thesis` and an `Antithesis`. Projects `mu` from the thesis and `lam` from the antithesis.

**bilattice**: a set ordered by two distinct partial orders — the truth order and the knowledge order. The unit square of `(mu, lam)` pairs forms a bilattice.

**FDE**: Belnap–Dunn four-valued logic. The logic of true, false, both (contradiction), and neither (indeterminacy).

**threshold**: the standard of evidence, `0.5` by default, used to classify a `TruthValue` into one of the four states.

**Aufhebung**: sublation. A value is sublated when it is no longer indeterminate — determined in some direction, whether by affirmation, denial, or standing contradiction.
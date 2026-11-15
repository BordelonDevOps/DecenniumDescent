# CHR-03 earned Cleric advancement source/API gate

**Source/API review requested; runtime implementation is not authorized by this packet.** This follows actual CHR-02 acceptance `84bd8644-f237-55a4-8d15-c8a18ddda017`, implementation `6063d8073c3bdd16ef9a7b70e8dd31aac2f96653`, final evidence `f10088757bbc89da2f4ecd36f0974b456d2620ac`, and acknowledgment baseline `29eed15d770de93f00217a0d9977c5bb489cfca4`.

The selected successor is one earned Cleric 1 → 2 advancement from the accepted companion. Its direct mapped prerequisite remains CHR-02. The audit identifies the mandatory Invocation choice/active path bonus, two additional Base selections, the earned milestone, and the spell-repertoire obligation. The authored example's optional Conviction Pool selection also needs a real capacity representation without inventing a current Conviction balance.

[Contract and concrete review decisions](SOURCE_API_CONTRACT.md) describe the target connected transaction, source obligations, missing capabilities, and proposed preannounced TEST_ONLY milestone. [Exact source and baseline bindings](SOURCE_API_BINDINGS.json) and [validation](CONTRACT_VALIDATION.json) bind the evidence. The validation checks source facts and unchanged engine files; it is not compilation, a gameplay test, or proof of runtime completion.

No engine code, save schema, character facts, funding, source authority or release status changes here. Runtime advancement stays closed until the reviewer resolves the identified dependencies and approves a complete contract. TAC-07/TAC-08 remain their own branch; no silent dependency reorder is made. The full C# engine goal remains active and Unity gameplay integration stays deferred.

Verifier development correction: the first source audit stopped because it compared prerequisite arrays as an execution sequence. TAC-08's map lists TAC-02/TAC-05/TAC-07; the contract lists the same three edges in another order. The verifier now compares exact prerequisite edges without imposing an extra order. The map, sources and engine were unchanged; this was not a runtime test failure or a relaxation of any dependency.

(glossary)=
# Glossary

```{glossary}
CAR
  Content Addressable aRchive. A file format which can store many {term}`CID`s and their content in one file (like TAR). See also [CARv1 Specification](https://ipld.io/specs/transport/car/carv1/).

CID
  Content IDentifier. A label to identify content, based on a cryptographic hash. The referenced content thus becomes immutable and verifiable. See also [What is a CID?](https://docs.ipfs.tech/concepts/content-addressing/#what-is-a-cid).

IPFS
  A decentralized system for retrieving content addressed data. See also [What is IPFS?](https://docs.ipfs.tech/concepts/what-is-ipfs/), and [IPFS@ORCESTRA](IPFS).

pinning
  A method to tell an {term}`IPFS` node that it should **retrieve and keep** the content behind a {term}`CID`. See also [Pinning](https://docs.ipfs.tech/concepts/glossary/#pinning).

pinning service
  A service running an {term}`IPFS` node (usually at a well-connected place) and offers {term}`pinning` to other users. See also [Pinning service](https://docs.ipfs.tech/concepts/glossary/#pinning-service).
```

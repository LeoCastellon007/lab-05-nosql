// Case Study 1: The Bookstore's New Inventory System (mongosh)
// Run from the repository's top-level directory so authors.json and books.json resolve:
//   mongosh "$MONGODB_ATLAS_URL" --apiVersion 1 --username "$MONGODB_ATLAS_USER" --file bookstore.js

// Step 2: switch to the bookstore database
// use bookstore
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)

// Step 4: load books.json
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)

// Step 5: list authors and books
// printjson is needed so results show when the file is run with load() or --file
printjson(db.authors.find().toArray())
printjson(db.books.find().toArray())

// Step 6: insert two new books
// Coraline is by an existing author (Neil Gaiman, author_002).
// The Long Earth is co-written by an existing author (Terry Pratchett, author_003)
// and a new author (Stephen Baxter, author_004).
db.books.insertMany([
  {
    title: "Coraline",
    published_year: 2002,
    author_ids: ["author_002"]
  },
  {
    title: "The Long Earth",
    published_year: 2012,
    author_ids: ["author_003", "author_004"]
  }
])

// Step 7: add missing authors
// author_004 is referenced by The Long Earth but not in the authors collection yet
db.authors.insertOne({
  _id: "author_004",
  name: "Stephen Baxter",
  nationality: "British",
  bio: {
    short: "British author of hard science fiction.",
    long: "Stephen Baxter is a British science fiction author with a background in mathematics and engineering. He is known for the Xeelee Sequence and co-wrote The Long Earth series with Terry Pratchett."
  }
})

// Step 8: filter books by a list of authors
// author_001 is from the loaded files; author_004 was added in step 7
printjson(db.books.find({ author_ids: { $in: ["author_001", "author_004"] } }).toArray())

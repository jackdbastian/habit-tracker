/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("mtmi6b5usds4a16")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "g3umdafv",
    "name": "release_id",
    "type": "text",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("mtmi6b5usds4a16")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "g3umdafv",
    "name": "discogs_id",
    "type": "text",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  return dao.saveCollection(collection)
})

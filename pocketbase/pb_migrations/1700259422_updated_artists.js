/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8susz1j99psxbcb")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "xwptvabm",
    "name": "artist_id",
    "type": "relation",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "collectionId": "8susz1j99psxbcb",
      "cascadeDelete": false,
      "minSelect": null,
      "maxSelect": 1,
      "displayFields": null
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8susz1j99psxbcb")

  // remove
  collection.schema.removeField("xwptvabm")

  return dao.saveCollection(collection)
})

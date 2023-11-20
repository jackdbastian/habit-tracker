/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8susz1j99psxbcb")

  // remove
  collection.schema.removeField("z1x6cijj")

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8susz1j99psxbcb")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "z1x6cijj",
    "name": "artist_id",
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

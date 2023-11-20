/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("1gvw05vc7r2uhbu")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "ytbxczt6",
    "name": "company_id",
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
  const collection = dao.findCollectionByNameOrId("1gvw05vc7r2uhbu")

  // remove
  collection.schema.removeField("ytbxczt6")

  return dao.saveCollection(collection)
})

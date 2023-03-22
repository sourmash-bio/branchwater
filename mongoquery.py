import pymongo as pm


def getmongo(acc_t, meta_list):
    client = pm.MongoClient("mongodb://localhost:27017/")
    db = client["sradb"]  # get db
    sradb_col = db["sradb_list"]  # get collection

    meta_dict = {'_id': 0}
    for item in meta_list:
        meta_dict[item] = 1

    testquery2 = list(sradb_col.find(
        {'acc': {"$in": acc_t}}, meta_dict))

    return (testquery2)

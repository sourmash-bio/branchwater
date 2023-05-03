import pymongo as pm


def getmongo(acc_t, meta_list):
    # connect to client and get collection
    client = pm.MongoClient("mongodb://localhost:27017/")
    db = client["sradb"]
    sradb_col = db["sradb_list"]

    # deselect ID; return acc and biosample html for every query
    meta_dict = {'_id': 0, 'acc': 1, 'biosample_link': 1}
    for item in meta_list:
        meta_dict[item] = 1

    testquery2 = list(sradb_col.find(
        {'acc': {"$in": acc_t}}, meta_dict))

    return (testquery2)

@app.route("/api/menu/food/<int:entity_id>", methods=["GET"])
def get_food(entity_id):
      entity = core.find_food(entity_id)
      if entity:
        return {
                "success": True, 
                "message": "", 
                "code": 0, 
                "data": entity
                }
      else:
         raise EntryNotFound(msg="Entry not found", entity_id=entity_id)
         return {
                "success": False,
                "message": "Entry not found",
                "code": ErrorCodes.ENTRY_NOT_FOUND,
                "data": {}
                }, 404

@app.route("/api/menu/food", methods=["POST"])
def post_food():
        data = request.get_json()
        food_data = data.get("food")
        name = food_data.get("food_name")
        price = food_data.get("price")
        category = food_data.get("category")
        size = food_data.get("food_size")
        try:
            food = core.create_food(name, price, category, food_size=size)
        except Exception as e:
            logging.ERROR(e)
            return {
                "success": False, 
                "message": "An unexpected error occurred",
                "code": ErrorCodes.GENERIC_SERVER_ERROR,
                "data": {}
                }, 500
        if food:
            return {
                "success": True,
                "message": "", 
                "code": 0,
                "data": food
                }
        else:
            return {
                "success": False,
                "message": "Food size is required for this category", 
                "code": ErrorCodes.MISSING_FOOD_SIZE,
                "data": {}
                }, 400

@app.route("/api/menu/food/<int:entity_id>", methods=["DELETE"])
def delete_food(entity_id):
    try:
        food = core.delete_food(entity_id)
    except:
        return {
            "success": False,
            "message": "An unexpected error occurred",
            "code": ErrorCodes.GENERIC_SERVER_ERROR,
            "data": {}
            }, 500
    if food:
        return {
            "success": True,
            "message": "",
            "code": 0,
            "data": {}
            }
    else:
        return {
            "success": False,
            "message": "Entry not found",
            "code": ErrorCodes.ENTRY_NOT_FOUND,
            "data": {}
            }, 404
    
@app.route("/api/menu/food/<int:entity_id>", methods=["PUT"])
def update_food(entity_id):
    data = request.get_json()
    if not data.get("food"):
        return {
            "success": False,
            "message": "No data provided",
            "code": ErrorCodes.MISSING_FOOD_DATA,
            "data": {}
            }, 400
    food_data = data.get("food")

    food_entity = core.find_food(entity_id)
    if not food_entity:
        return {
            "success": False,
            "message": "Entry not found",
            "code": ErrorCodes.ENTRY_NOT_FOUND,
            "data": {}
            }, 404

    try:
        food = core.update_food_name(entity_id, data.get("food"))
    except:
        return {
            "success": False,
            "message": "An unexpected error occurred",
            "code": ErrorCodes.GENERIC_SERVER_ERROR,
            "data": {}
            }, 500

    if not food:
        logging.error("Food entity exists, but when attempted to be updated, the entity was not found.")
        logging.error(f"Entity ID: {entity_id}\nData: {data}")
        return {
            "success": False,
            "message": "An unexpected error occurred",
            "code": ErrorCodes.GENERIC_SERVER_ERROR,
        }, 500

    response = {"success": True, "message": "", "code": 0, "data": []}

    food_data = data.get("food")
    name = food_data.get("food_name")
    price = food_data.get("price")
    category = food_data.get("category")
    size = food_data.get("food_size")
        
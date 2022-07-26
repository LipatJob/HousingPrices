nominal_columns = {
    "MSSubClass",
    "MSZoning",  # can be decomposed
    "Street",
    "Alley",
    "LandContour",
    "LotConfig",
    "Neighborhood",
    "Condition1",
    "Condition2",
    "BldgType",
    "HouseStyle",
    "RoofStyle",
    "RoofMatl",
    "Exterior1st",
    "Exterior2nd",
    "MasVnrType",
    "Foundation",
    "Heating",
    "CentralAir",
    "Electrical",
    "GarageType",
    "PavedDrive",
}

ordinal_columns = {
    "LotShape",  # !!
    "Utilities",  # !!
    "LandSlope",
    "ExterQual",
    "ExterCond",
    "BsmtQual",
    "BsmtCond",
    "BsmtExposure",
    "BsmtFinType1",
    "BsmtFinType2",
    "HeatingQC",
    "KitchenQual",
    "Functional",
    "FireplaceQu",
    "GarageFinish",
    "GarageQual",
    "GarageCond",
    "PoolQC",
    "Fence",
    "MiscFeature",
    "SaleType",
    "SaleCondition",
}

mapped_ordinal_columns = {
    "OverallQual",
    "OverallCond",
}


numerical_columns = {
    "LotFrontage",
    "LotArea",
    "MasVnrArea",
    "BsmtFinSF1",
    "BsmtFinSF2",
    "BsmtUnfSF",
    "TotalBsmtSF",
    "1stFlrSF",
    "2ndFlrSF",
    "LowQualFinSF",
    "GrLivArea",
    "BsmtFullBath",
    "BsmtHalfBath",
    "FullBath",
    "HalfBath",
    "TotRmsAbvGrd",
    "Fireplaces",
    "GarageCars",
    "GarageArea",
    "WoodDeckSF",
    "OpenPorchSF",
    "EnclosedPorch",
    "3SsnPorch",
    "ScreenPorch",
    "PoolArea",
    "MiscVal",
    "YearBuilt",
    "YearRemodAdd",
    "GarageYrBlt",
    "MoSold",
    "YrSold",
    "BedroomAbvGr",  # MISSING DESCRIPTION
    "KitchenAbvGr"  # MISSING DESCRIPTION
}


def get_column_mappings():
    content = []
    with open("data/data_description.txt") as f:
        content = f.readlines()
    title_rows = []
    label_blocks = []

    i = 0

    NEW_LINE = "\n"

    TITLE_STATE = 1
    BETWEEN_TITLE_BLOCK_STATE = 2
    BETWEEN_GROUP_STATE = 2
    LABEL_BLOCK_STATE = 3
    current_state = TITLE_STATE
    while i < len(content):
        next_state = None
        line = content[i]
        if current_state == TITLE_STATE:
            title_rows.append(line)
            label_blocks.append([])
            next_state = BETWEEN_TITLE_BLOCK_STATE
        elif current_state == BETWEEN_TITLE_BLOCK_STATE:
            if i + 1 >= len(content):
                break
            next_line = content[i + 1]
            if ":" in next_line:
                next_state = TITLE_STATE
            else:
                next_state = LABEL_BLOCK_STATE
        elif current_state == LABEL_BLOCK_STATE:
            if i + 1 >= len(content):
                break
            next_line = content[i + 1]

            if next_line.replace("\t", "").replace(" ", "") == NEW_LINE:
                label_blocks[-1].append(line)
                next_state = BETWEEN_GROUP_STATE
            else:
                label_blocks[-1].append(line)
                next_state = LABEL_BLOCK_STATE

        elif current_state == BETWEEN_GROUP_STATE:
            next_state = TITLE_STATE
        current_state = next_state
        i += 1

    titles = []
    for title in title_rows:
        titles.append(title.split(":")[0].strip())
    label_groups = []
    for label_data in label_blocks:
        label_groups.append([label_row.replace("       ", "").replace(
            "\n", "").split("\t")[0].strip() for label_row in label_data])

    ordinal_mapping = {}
    for title, labels in zip(titles, label_groups):
        indices = {label: i for label, i in zip(
            labels, reversed(range(0, len(labels))))}
        ordinal_mapping[title] = indices
    return ordinal_mapping

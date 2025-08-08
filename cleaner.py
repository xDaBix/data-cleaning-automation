import pandas as pd

def clean_data(
    df,
    selected_columns=None,
    numeric_fill_strategy='mean',
    categorical_fill_strategy='mode',
    cat_fill_constant=None,
    remove_outliers=False,
    duplicate_removal='full row',
    duplicate_columns=None
):
    # Normalize column names early
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

    # Work on a copy
    df = df.copy()

    # Handle duplicate removal
    if duplicate_removal == 'full row':
        df = df.drop_duplicates()
    elif duplicate_removal == 'specific columns' and duplicate_columns:
        # Make sure duplicate_columns are normalized too
        duplicate_columns = [col.strip().lower().replace(' ', '_') for col in duplicate_columns]
        df = df.drop_duplicates(subset=duplicate_columns)
    # else 'none' => keep duplicates

    # If no selected columns given, use all
    if selected_columns is None:
        selected_columns = df.columns.tolist()
    else:
        # Normalize selected columns as well
        selected_columns = [col.strip().lower().replace(' ', '_') for col in selected_columns]

    # Identify numeric and categorical cols from selected columns
    numeric_cols = [col for col in selected_columns if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
    categorical_cols = [col for col in selected_columns if col in df.columns and pd.api.types.is_object_dtype(df[col])]

    # Numeric fill or drop
    if numeric_fill_strategy == 'drop':
        df = df.dropna(subset=numeric_cols)
    else:
        for col in numeric_cols:
            if numeric_fill_strategy == 'mean':
                df[col] = df[col].fillna(df[col].mean())
            elif numeric_fill_strategy == 'median':
                df[col] = df[col].fillna(df[col].median())

    # Clean categorical columns: strip/lower
    for col in categorical_cols:
        # Convert to string first (to handle NaNs), then strip and lower
        df[col] = df[col].astype(str).str.strip().str.lower()

        # Treat 'nan', '', and 'none' as missing values
        df.loc[df[col].isin(['nan', '', 'none']), col] = pd.NA

    # Handle categorical fill or drop
    if categorical_fill_strategy == 'drop':
        df = df.dropna(subset=categorical_cols)
    else:
        for col in categorical_cols:
            if categorical_fill_strategy == 'mode':
                mode = df[col].mode(dropna=True)
                fill_value = mode[0] if not mode.empty else "unknown"
            elif categorical_fill_strategy == 'constant':
                fill_value = cat_fill_constant if cat_fill_constant is not None else "unknown"
            else:
                fill_value = None  # should not happen

            if fill_value is not None:
                df[col] = df[col].fillna(fill_value)

    # Remove outliers (IQR method)
    if remove_outliers:
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    return df

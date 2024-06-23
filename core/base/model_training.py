import tensorflow as tf
from sklearn.model_selection import train_test_split

def build_model(num_users, num_intriguers):
    user_input = tf.keras.layers.Input(shape=(1,), name='user_input')
    intriguer_input = tf.keras.layers.Input(shape=(1,), name='intriguer_input')

    user_embedding = tf.keras.layers.Embedding(num_users, 50, input_length=1)(user_input)
    intriguer_embedding = tf.keras.layers.Embedding(num_intriguers, 50, input_length=1)(intriguer_input)

    user_flatten = tf.keras.layers.Flatten()(user_embedding)
    intriguer_flatten = tf.keras.layers.Flatten()(intriguer_embedding)

    concat = tf.keras.layers.Concatenate()([user_flatten, intriguer_flatten])
    dense_1 = tf.keras.layers.Dense(128, activation='relu')(concat)
    dense_2 = tf.keras.layers.Dense(64, activation='relu')(dense_1)
    output = tf.keras.layers.Dense(1, activation='sigmoid')(dense_2)

    model = tf.keras.Model(inputs=[user_input, intriguer_input], outputs=output)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model(df):
    user_ids = df['user_id'].unique().tolist()
    intriguer_ids = df['intriguer_id'].unique().tolist()

    user_id_mapping = {id: idx for idx, id in enumerate(user_ids)}
    intriguer_id_mapping = {id: idx for idx, id in enumerate(intriguer_ids)}

    df['user'] = df['user_id'].map(user_id_mapping)
    df['intriguer'] = df['intriguer_id'].map(intriguer_id_mapping)

    X = df[['user', 'intriguer']]
    y = df['liked']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = build_model(len(user_ids), len(intriguer_ids))
    model.fit([X_train['user'], X_train['intriguer']], y_train, epochs=10, batch_size=32, validation_data=([X_test['user'], X_test['intriguer']], y_test))

    return model, user_id_mapping, intriguer_id_mapping

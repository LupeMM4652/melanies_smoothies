# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders:cup_with_straw:")
st.write(
    """ Orders that need to be filled.
    """)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options"). select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

cnx = st.connection ("snowflake")
session = cnx.session()


if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    if submitted:
    
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        
        try:
            og_dataset.merge(edited_dataset
                         , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
            st.success('Someone clicked the button', icon = '👍')
        except:
            st.write('Something went wrong,' icon = '👎')

else: 
    st.success('There are no pending orders right now', icon = '✅')

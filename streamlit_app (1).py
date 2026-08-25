# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(f":cup_with_straw: Pending Smoothy Orders :cup_with_straw:")
st.write(
  """Orders that need to be filled.
  """
)

# setup the session 
# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

# COL fn to select single column and FILTER() 
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED") == 0).collect()

# only display table if there were unfilled orders
if my_dataframe:
 
    # display the retreived table
    #st.table(my_dataframe)
    editable_df = st.data_editor(my_dataframe)
                   
    # collect resuts
    submitted = st.button('Submit')

    if submitted:
        try:    
            # merge data
            og_dataset = session.table("smoothies.public.orders")
            edited_dataset = session.create_dataframe(editable_df)

            # add a bug to test exception
            # raise ValueError("forced break -- to ensure no save")
    
            og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] ==  edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
        except:
            st.write(
  """An error occured.
  """
)   
        else:
            st.success("Someone clicked the button", icon="👍")
        finally:
            st.write(
  """finished update attempt.
  """
) 
else: 
    st.success("There are no pending orders right now", icon="😐")
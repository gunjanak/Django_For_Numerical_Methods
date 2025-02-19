# Create your views here.
from django.views.generic.edit import FormView
from django.shortcuts import render
import plotly.express as px
import plotly.io as pio
import base64
from io import BytesIO


from .forms import StockSymbolForm
from .dataframe_nepse import stock_dataFrame
from .helper import prepare_data,just_test,train_and_test

def symbol_view(request):
    if request.method == 'POST':
        try:
            form = StockSymbolForm(request.POST)
            if form.is_valid():
                # Process the form data
                symbol = form.cleaned_data['text_input']
                df = stock_dataFrame(symbol)
                df_show = df.copy()
                df_show = df_show.reset_index()
                df_show['Date'] = df_show['Date'].dt.strftime('%b. %-d, %Y')
                head = df_show.head()
                tail = df_show.tail()
                df,model_path = prepare_data(df,symbol)
                print("***********%%%%%%%%%%%%%%%%%%%%%%%***********")
                # print(df.head())
                print(f"Model_path:{model_path}")
                
                # test_mape = just_test(df,model_path)
                # print(test_mape)
                
                # mape,test_mape,predicted_tomorrow_price_original = train_and_test(df,model_path)
                df_test,test_mape,predicted_tomorrow_price_original = just_test(df,model_path)
                
                print(test_mape)
                # Generate Plotly Figure
                fig = px.line(df_test, x=df_test.index, y=df_test.columns, title=f"Test Data for {symbol}")

                # Convert Plotly figure to HTML
                plot_html = pio.to_html(fig, full_html=False)
                  
                
                # Example processing logic (customize as needed)
                result = {
                    'symbol': symbol, 
                    'head':head,
                    'tail':tail,
                    'Test_MAPE':test_mape,
                    'Forcasted_Price':predicted_tomorrow_price_original, 
                    'plot_html': plot_html,
                    'model_path':model_path,
                }
                
                return render(request, 'stock.html', {'form':form,'result': result})
        except Exception as e:
            error_message = f"Error evaluating the formula: {str(e)}"
            print(error_message)
            context = {'form':form,'error_message':error_message}
            return render(request,'stock.html',context)
    else:
        form = StockSymbolForm()
    
    return render(request, 'stock.html', {'form': form})

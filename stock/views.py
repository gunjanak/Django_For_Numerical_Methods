# Create your views here.
from django.views.generic.edit import FormView
from django.shortcuts import render
from .forms import StockSymbolForm


from .dataframe_nepse import stock_dataFrame

def symbol_view(request):
    if request.method == 'POST':
        try:
            form = StockSymbolForm(request.POST)
            if form.is_valid():
                # Process the form data
                symbol = form.cleaned_data['text_input']
                df = stock_dataFrame(symbol)
                print(df)
                head = df.head()
                tail = df.tail()
                # Example processing logic (customize as needed)
                result = {
                    'symbol': symbol, 
                    'head':head,
                    'tail':tail,  
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

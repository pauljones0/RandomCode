import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fetch_stock_data(ticker_symbol, period="1y"):
    """
    Fetch daily stock data for a given ticker using yfinance.
    
    Parameters:
        ticker_symbol (str): The stock ticker (e.g., 'AAPL').
        period (str): Time period to fetch data (e.g., '1y', '6mo').
    
    Returns:
        DataFrame: Historical stock data with a 'Date' column.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period=period)
        if df.empty:
            raise Exception("No data returned for the ticker. Check the ticker symbol and period.")
        df.reset_index(inplace=True)  # Make sure 'Date' is a column
        return df, ticker
    except Exception as e:
        raise Exception(f"Error fetching stock data: {e}")

def fetch_eps_history(ticker_symbol):
    """
    Fetch historical EPS data using yfinance methods for more complete coverage.
    
    Parameters:
        ticker_symbol (str): The stock ticker symbol
    Returns:
        DataFrame: Historical EPS data with 'Date' and 'epsActual' columns
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # Try earnings_dates first (historical data)
        earnings_dates = ticker.earnings_dates
        if earnings_dates is not None and not earnings_dates.empty:
            eps_df = earnings_dates[['Reported EPS']].copy()
            eps_df = eps_df.rename(columns={'Reported EPS': 'epsActual'})
            eps_df.index.name = 'Date'
            eps_df = eps_df.reset_index()
            
        else:
            # Fallback to earnings_history
            earnings_history = ticker.earnings_history
            if earnings_history is not None and not earnings_history.empty:
                eps_df = earnings_history[['epsActual']].copy()
                eps_df.index.name = 'Date'
                eps_df = eps_df.reset_index()
            else:
                raise Exception("No earnings data available")
        
        # Convert index to datetime and ensure timezone-naive
        eps_df['Date'] = pd.to_datetime(eps_df['Date']).dt.tz_localize(None)
        
        # Only use historical EPS data (up to today)
        current_date = pd.Timestamp.now()
        eps_df = eps_df[eps_df['Date'] <= current_date]
        
        # Sort by date and remove any NaN values
        eps_df = eps_df.sort_values('Date').dropna(subset=['epsActual'])
        
        if eps_df.empty:
            raise Exception("No valid historical EPS data found")
            
        return eps_df
            
    except Exception as e:
        raise Exception(f"Error fetching EPS data: {e}")

def compute_dynamic_pe_ratio(stock_df, eps_df):
    """
    Merge the EPS history with the stock data and compute a dynamic P/E ratio.
    
    Parameters:
        stock_df (DataFrame): Daily stock data with a 'Date' and 'Close' column.
        eps_df (DataFrame): Quarterly EPS events with 'Date' and 'epsActual'.
        
    Returns:
        DataFrame: The stock data with additional 'epsActual' and 'P/E Ratio' columns.
    """
    # Ensure both DataFrames have timezone-naive datetime
    stock_df = stock_df.copy()
    stock_df['Date'] = pd.to_datetime(stock_df['Date']).dt.tz_localize(None)
    
    # Filter eps_df to include one entry before start_date (if exists) plus all entries during the period
    mask = (eps_df['Date'] <= eps_df['Date'].max())
    filtered_eps = eps_df[mask].copy()
    
    # Merge stock data with EPS events
    merged_df = pd.merge_asof(stock_df.sort_values('Date'),
                             filtered_eps.sort_values('Date'),
                             on='Date',
                             direction='backward')
    
    # Compute P/E ratio where epsActual is valid and non-zero
    merged_df['P/E Ratio'] = merged_df.apply(
        lambda row: row['Close'] / row['epsActual'] if pd.notnull(row['epsActual']) and row['epsActual'] != 0 else None,
        axis=1
    )
    
    return merged_df

def compute_roi(df):
    """
    Compute the Return on Investment (ROI) based on the first and last 'Close' prices.
    
    ROI is calculated as: (Final Price - Initial Price) / Initial Price.
    """
    if df.empty:
        raise Exception("Dataframe is empty. Cannot compute ROI.")
    initial_price = df['Close'].iloc[0]
    final_price = df['Close'].iloc[-1]
    roi = (final_price - initial_price) / initial_price
    return roi

def compute_volatility(df, annualize=True):
    """
    Compute the volatility of stock returns.
    
    Volatility is measured as the standard deviation of daily returns.
    If annualize is True, multiply by sqrt(252) assuming 252 trading days per year.
    """
    df['Daily Return'] = df['Close'].pct_change()
    daily_vol = df['Daily Return'].std()
    if annualize:
        return daily_vol * np.sqrt(252)
    return daily_vol

def compute_moving_average(df, window=20):
    """
    Compute the moving average for closing prices over a specified window.
    """
    df[f'MA_{window}'] = df['Close'].rolling(window=window).mean()
    return df

def visualize_data(df, root_window):
    """
    Generate visualizations in a maximized window with control buttons.
    """
    # Create a new window for the plot
    plot_window = tk.Toplevel(root_window)
    plot_window.title("Stock Analysis Results")
    
    # Add protocol handler for window close button
    plot_window.protocol("WM_DELETE_WINDOW", lambda: [plot_window.destroy(), root_window.quit()])
    
    # Make window maximized
    plot_window.state('zoomed')  # Windows
    # plot_window.attributes('-zoomed', True)  # Linux
    
    # Create main frame
    main_frame = ttk.Frame(plot_window)
    main_frame.pack(fill='both', expand=True)
    
    # Create matplotlib figure
    fig = plt.figure(figsize=(14, 12))
    
    # Price and moving average plot
    plt.subplot(2, 1, 1)
    sns.lineplot(x='Date', y='Close', data=df, 
                linewidth=1.5, 
                color='#1f77b4',
                label='Close Price')
    if 'MA_20' in df.columns:
        sns.lineplot(x='Date', y='MA_20', data=df, 
                    linewidth=1.5, 
                    color='#2ca02c',
                    label='20-Day MA')
    plt.title('Stock Close Price Over Time', pad=20, fontsize=12)
    plt.xlabel('Date', fontsize=10)
    plt.ylabel('Price', fontsize=10)
    plt.legend(fontsize=9, loc='upper right')
    plt.grid(True, alpha=0.3)
    
    # Dynamic P/E ratio and EPS plot
    plt.subplot(2, 1, 2)
    
    # Create twin axes for P/E and EPS
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    
    # Plot EPS
    valid_eps = df.dropna(subset=['epsActual'])
    sns.lineplot(x='Date', y='epsActual', data=valid_eps, 
                linewidth=1.5, 
                color='#0047AB',
                linestyle='--',
                alpha=0.8,
                label='EPS', 
                ax=ax2)
    ax2.set_ylabel('EPS', color='#0047AB', fontsize=10)
    ax2.tick_params(axis='y', labelcolor='#0047AB')
    ax2.grid(False)
    
    # Plot P/E ratio
    valid_pe = df.dropna(subset=['P/E Ratio'])
    sns.lineplot(x='Date', y='P/E Ratio', data=valid_pe, 
                linewidth=2.5,
                color='#ff7f0e',
                label='P/E Ratio', 
                ax=ax1)
    ax1.set_ylabel('P/E Ratio', color='#ff7f0e', fontsize=10)
    ax1.tick_params(axis='y', labelcolor='#ff7f0e')
    
    # Customize grid
    ax1.grid(True, alpha=0.2)
    
    # Add both legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, 
              loc='upper right',
              fontsize=9,
              framealpha=0.9)
    
    # Remove the second legend from ax2
    ax2.get_legend().remove()
    
    plt.title('Dynamic P/E Ratio and EPS Over Time', pad=20, fontsize=12)
    plt.xlabel('Date', fontsize=10)
    
    # Adjust layout
    plt.tight_layout()
    
    # Create canvas
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    # Create button frame
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=10)
    
    # Add control buttons
    ttk.Button(
        button_frame,
        text="Analyze Another Stock",
        command=lambda: [plot_window.destroy(), root_window.deiconify()],
        style='Accent.TButton'
    ).pack(side='left', padx=5)
    
    ttk.Button(
        button_frame,
        text="Exit",
        command=lambda: [plot_window.destroy(), root_window.quit()],
        style='Accent.TButton'
    ).pack(side='left', padx=5)
    
    # Center the window
    plot_window.update_idletasks()
    width = plot_window.winfo_width()
    height = plot_window.winfo_height()
    x = (plot_window.winfo_screenwidth() // 2) - (width // 2)
    y = (plot_window.winfo_screenheight() // 2) - (height // 2)
    plot_window.geometry(f'+{x}+{y}')

class StockAnalysisGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stock Analysis Tool")
        self.root.geometry("400x500")
        self.root.configure(bg='#f0f0f0')
        
        # Center the main window
        self.center_window(self.root)
        
        # Configure style with modern aesthetics
        self.setup_styles()
        
        self.setup_main_window()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern button style
        style.configure('Accent.TButton',
                       padding=10,
                       background='#2196F3',
                       foreground='white',
                       font=('Helvetica', 11))
        
        # Configure modern entry style
        style.configure('TEntry',
                       padding=5,
                       fieldbackground='white',
                       font=('Helvetica', 11))
        
        # Configure modern radio button style
        style.configure('TRadiobutton',
                       background='#f0f0f0',
                       font=('Helvetica', 10))
    
    def center_window(self, window):
        """Center any window on the screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

    def setup_main_window(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#f0f0f0')
        title_frame.pack(pady=20)
        tk.Label(
            title_frame,
            text="Stock Analysis Tool",
            font=('Helvetica', 24, 'bold'),
            bg='#f0f0f0'
        ).pack()

        # Input Frame
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(pady=20, padx=40, fill='x')

        # Stock Ticker
        tk.Label(
            input_frame,
            text="Stock Ticker:",
            font=('Helvetica', 12),
            bg='#f0f0f0'
        ).pack(anchor='w')
        
        self.ticker_entry = ttk.Entry(input_frame, font=('Helvetica', 12))
        self.ticker_entry.pack(fill='x', pady=(5, 15))

        # Time Period
        tk.Label(
            input_frame,
            text="Time Period:",
            font=('Helvetica', 12),
            bg='#f0f0f0'
        ).pack(anchor='w')

        # Period Selection Frame
        period_frame = tk.Frame(input_frame, bg='#f0f0f0')
        period_frame.pack(fill='x', pady=5)

        self.period_var = tk.StringVar(value="1y")
        periods = [
            ("1 Month", "1mo"),
            ("3 Months", "3mo"),
            ("6 Months", "6mo"),
            ("1 Year", "1y"),
            ("2 Years", "2y"),
            ("5 Years", "5y"),
        ]

        for text, value in periods:
            ttk.Radiobutton(
                period_frame,
                text=text,
                value=value,
                variable=self.period_var
            ).pack(anchor='w', pady=2)

        # Analyze Button
        ttk.Button(
            self.root,
            text="Analyze Stock",
            command=self.validate_and_analyze,
            style='Accent.TButton'
        ).pack(pady=20)

    def setup_loading_window(self):
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.title("Analyzing...")
        self.loading_window.geometry("300x200")
        self.loading_window.configure(bg='#f0f0f0')
        
        # Remove window decorations and make it float
        self.loading_window.overrideredirect(True)
        
        # Center loading window
        self.center_window(self.loading_window)
        
        # Create a frame with border
        frame = tk.Frame(self.loading_window, bg='#f0f0f0',
                        highlightbackground='#2196F3',
                        highlightthickness=2)
        frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Loading message
        tk.Label(
            frame,
            text="Analyzing Stock Data...",
            font=('Helvetica', 14, 'bold'),
            bg='#f0f0f0',
            fg='#2196F3'
        ).pack(pady=20)
        
        # Progress bar with custom style
        style = ttk.Style()
        style.configure('Blue.Horizontal.TProgressbar',
                       troughcolor='#f0f0f0',
                       background='#2196F3',
                       thickness=10)
        
        self.progress = ttk.Progressbar(
            frame,
            mode='indeterminate',
            length=200,
            style='Blue.Horizontal.TProgressbar'
        )
        self.progress.pack(pady=20)
        self.progress.start(10)

    def validate_ticker(self, ticker):
        try:
            ticker = ticker.upper().strip()
            stock = yf.Ticker(ticker)
            # Try to get info to validate ticker
            info = stock.info
            return True, ticker
        except:
            return False, None

    def validate_and_analyze(self):
        ticker = self.ticker_entry.get().strip()
        
        # Validate ticker
        is_valid, validated_ticker = self.validate_ticker(ticker)
        if not is_valid:
            messagebox.showerror(
                "Invalid Ticker",
                "Please enter a valid stock ticker symbol."
            )
            return

        # Show loading window
        self.setup_loading_window()
        
        # Start analysis in a separate thread
        thread = threading.Thread(
            target=self.run_analysis,
            args=(validated_ticker, self.period_var.get())
        )
        thread.daemon = True
        thread.start()

    def run_analysis(self, ticker, period):
        try:
            # Run the existing analysis code
            stock_df, ticker_obj = fetch_stock_data(ticker, period)
            eps_df = fetch_eps_history(ticker)
            
            if eps_df is not None and not eps_df.empty:
                stock_df = compute_dynamic_pe_ratio(stock_df, eps_df)
            
            stock_df = compute_moving_average(stock_df, window=20)
            
            # Close loading window and show results
            self.root.after(0, self.show_results, stock_df)
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))

    def show_results(self, stock_df):
        self.loading_window.destroy()
        self.root.withdraw()  # Hide main window while showing plot
        visualize_data(stock_df, self.root)

    def show_error(self, error_message):
        self.loading_window.destroy()
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        error_window.configure(bg='#f0f0f0')
        
        # Center error window
        error_window.geometry("400x200")
        self.center_window(error_window)
        
        # Create frame with border
        frame = tk.Frame(error_window, bg='#f0f0f0',
                        highlightbackground='#ff5252',
                        highlightthickness=2)
        frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Error icon (you can replace with an actual image)
        tk.Label(
            frame,
            text="⚠️",
            font=('Helvetica', 48),
            bg='#f0f0f0'
        ).pack(pady=(20, 10))
        
        # Error message
        tk.Label(
            frame,
            text=f"An error occurred:\n{error_message}",
            font=('Helvetica', 11),
            wraplength=350,
            bg='#f0f0f0'
        ).pack(pady=10)
        
        # OK button
        ttk.Button(
            frame,
            text="OK",
            command=error_window.destroy,
            style='Accent.TButton'
        ).pack(pady=20)

    def run(self):
        self.root.mainloop()

def main():
    app = StockAnalysisGUI()
    app.run()

if __name__ == "__main__":
    main()

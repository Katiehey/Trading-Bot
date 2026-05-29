import matplotlib.pyplot as plt


def equity_curve(df, title="Equity Curve"):
    plt.figure(figsize=(12, 5))
    plt.plot(df["equity"], label="Equity")

    #Add trade markers to equity curve
    buys = df[df["signal"] == 1]
    sells = df[df["signal"] == -1]

    plt.scatter(buys.index, buys["equity"], marker="^", color="green")
    plt.scatter(sells.index, sells["equity"], marker="v", color="red")

    plt.legend()
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.grid(True)
    plt.show()


def drawdown_plot(df, title="Drawdown"):
    rolling_max = df["equity"].cummax()
    drawdown = (df["equity"] - rolling_max) / rolling_max

    plt.figure(figsize=(12, 4))
    plt.fill_between(drawdown.index, drawdown, 0)
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.show()

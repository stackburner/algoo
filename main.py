from __future__ import absolute_import, division, print_function, unicode_literals
import backtrader as bt
import backtrader.feeds as btfeeds
from data_api import Reader


class Strategy(bt.Strategy):

    def start(self):
        self.dataclose = self.datas[0].close
        self.p.monthly_cash = 100.0
        self.broker.set_fundmode(fundmode=True)
        self.cash_start = self.broker.get_cash()
        self.add_timer(
            bt.timer.SESSION_END,
            monthdays=[15], #day in the month for the execution
            monthcarry=True,
        )

    def notify_timer(self, timer, when, *args, **kwargs):
        self.broker.add_cash(self.p.monthly_cash)
        self.buy(size=self.p.monthly_cash/self.dataclose[0])


def get_data(ticker):
    df, path = Reader().a_get_daily(ticker)
    data = bt.feeds.GenericCSVData(dataname=path,
                                    tmformat=None,
                                    dtformat='%Y-%m-%d',
                                    datetime=0,
                                    open=1,
                                    high=2,
                                    low=3,
                                    close=5,
                                    volume=6,
                                    reverse=True)

    return data


def run_backtest():
    cerebro = bt.Cerebro()
    cerebro.adddata(get_data('SPY')) #IWLE.DE
    cerebro.addstrategy(Strategy)
    cerebro.broker.setcash(1000)
    cerebro.broker.setcommission(commission=0.015)
    print('Starting Portfolio Value: {0}'.format(cerebro.broker.getvalue()))
    cerebro.run()
    print('Final Portfolio Value: {0}'.format(cerebro.broker.getvalue()))
    cerebro.plot()


run_backtest()

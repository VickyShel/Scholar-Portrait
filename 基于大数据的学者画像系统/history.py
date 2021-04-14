from pyecharts import options as opts
from pyecharts.charts import Radar, Timeline
from pyecharts.faker import Faker
import dat


def getHistory(scholar):
    tl = Timeline()
    tl.add_schema(play_interval=500)
    for i in range(2015, 2021):
        total = dat.get_info_by_name(scholar)
        data = [[total[i-2010][3], total[i-2010][4], total[i-2010]
                 [5], total[i-2010][6], total[i-2010][7]]]
        pie = (
            Radar(init_opts=opts.InitOpts(width="450px",
                                          height="450px", bg_color="#F0F0F0"))
            # Radar()
            # .set_colors(["#4587E7"])
            .add_schema(
                schema=[
                    opts.RadarIndicatorItem(name="PaperNum", max_=600),
                    opts.RadarIndicatorItem(name="CitationNum", max_=5000),
                    opts.RadarIndicatorItem(name="H-index", max_=100),
                    opts.RadarIndicatorItem(name="P-index", max_=1),
                    opts.RadarIndicatorItem(name="G-index", max_=50),
                ],
                splitarea_opt=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
                textstyle_opts=opts.TextStyleOpts(color="#696969"),
            )
            .add(
                series_name="学者影响力",
                data=data,
                linestyle_opts=opts.LineStyleOpts(color="#696969", width="3"),

            )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts(title=""), legend_opts=opts.LegendOpts()
            )
        )
        tl.add(pie, "{}年".format(i))
    return tl

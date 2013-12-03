"""A sample XBlock for displaying a histogram of answer distributions for all problems."""

import pkg_resources
import json
import base64
import requests
from collections import defaultdict

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment

from matplotlib.pyplot import title, bar, savefig, clf, subplots, xticks, ylim, legend
from numpy import arange, random
from StringIO import StringIO

import logging
log = logging.getLogger(__name__)

class AnswerDistHistogramBlock(XBlock):
    """
    A sample XBlock for displaying a histogram of answer distributions for all problems.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    query_url = String(help="URL for Insights query", default="http://localhost:8002/query/all_problem_answers", scope=Scope.user_state_summary)
    title = String(help="Title for Answer Distribution Histogram", default="Problem-Answer Distribution for Course", scope=Scope.user_state_summary)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        The primary view of the AnswerDistHistogramBlock.

        At present, this encodes the image data as a string, and
        passes to the HTML template for rendering.

        In the future, it would be preferable to use a handler that
        serves up the image data as binary. That would a) cut down on
        bandwidth, and b) allow one to make the image auto-refresh.
        """
        sio_buffer = StringIO()
        self.write_histogram_to_buffer(sio_buffer)
        encoded_image_data = self.encode_image_data('png', sio_buffer.getvalue())
        sio_buffer.close()

        html = self.resource_string("static/html/answerhisto.html")
        frag = Fragment(html.format(encoded_image_data=encoded_image_data))
        frag.add_css(self.resource_string("static/css/answerhisto.css"))
        frag.add_javascript(self.resource_string("static/js/src/answerhisto.js"))
        frag.initialize_js('AnswerDistHistogramBlock')
        return frag

    def write_histogram_to_buffer(self, buffer):
        """
        Construct histogram and stream to provided buffer
        (as a file-like object).

        If the insights server is down or not responding to the
        specified query, this generates an empty plot and appends
        a warning to the title.

        NOTE: this functionality is not thread-safe.  Calls are made
        to matplotlib for the "current" plot, and if two histograms
        are generated at the same time, they could collide.
        """

        # fetch data from query:
        problems = self.get_answers_by_problem()
        
        # handle case if no data is fetched:
        if problems is None:
            title(self.title + ' (No Data Available)')
            # Write out empty plot to the buffer, and clear state. 
            savefig(buffer)
            clf()
            return

        fig, ax = subplots()
        # Semi-arbitrary
        bar_width = 0.25

        # The maximum count of any response.  Used to scale the y-axis.
        max_value = 0

        # Keeps track of the location along the x-axis where the histogram should be
        # rendered.  Note this increases with each rendered problem.
        problem_x_offset = 0

        # Stores the labels for the bars.  Will appear below the x-axis.
        x_tick_locations = []
        x_tick_labels = []

        for problem, values in problems.iteritems():
            log.info("Problem %s has values %s", problem, values)

            # Calculate the left coordinates of each of the bars.
            # problem_x_offset is the left coordinate of the problem
            # The resulting list should look like: 
            # [problem_x_offset, problem_x_offset + bar_width, problem_x_offset + (bar_width*2), ...]
            bar_index = arange(0, len(values)*bar_width, bar_width) + problem_x_offset
    
            # Calculate the maximum count seen across all problems, this will
            # be used to determine the scale of the y-axis.
            max_value_for_this_problem = max(values.values())
            max_value = max(max_value_for_this_problem, max_value)
    
            # Generate the plot
            bar(bar_index, values.values(), bar_width,
                label=problem,
                color=random.rand(3,))  # Use a random color
    
            # Gather labels for the x-axis with the various responses seen
            x_tick_locations.extend(bar_index + (bar_width/2))
            x_tick_labels.extend(values.keys())
    
            # Put an empty bar_width of space between histograms for each problem
            problem_x_offset = bar_index.max() + (bar_width*2)

        # Render the x-axis labels at an angle with the right most
        # letter centered under the bar
        xticks(x_tick_locations, x_tick_labels, rotation=50, ha='right')

        # Render some empty space above the top of the highest bar
        ylim(0, max_value*1.25)

        # Increase the size of the plot
        fig.set_size_inches(16, 14)

        # Add a legend and title
        legend()
        title(self.title)

        # Write out the plot to a buffer, and clear state. 
        savefig(buffer)
        clf()

    def encode_image_data(self, image_type, image_string):
        """
        Convert buffer contents to a form where it can be used as a
        'src' attribute of an <img> tag.  This involves converting
        to base64, and labelling with the appropriate mimetype.
        """
        value = base64.b64encode(image_string)
        return "data:image/{};base64, {}".format(image_type, value)

    def get_answers_by_problem(self):
        """
        Fetch the histogram data based on the query provided, and
        format into a dict keyed by problem, with a dict of
        answer/counts per problem.
        """
        url = self.query_url

        try:
            res = requests.get(url, timeout=30)
        except Exception:
            log.exception("Error trying to access analytics at %s", url)
            return None

        if res.status_code == requests.status_codes.codes.OK:
            problems = defaultdict(dict)
            for bucket in res.json():
                question = bucket['question']
                answer = bucket['answer']
                if isinstance(answer, list):
                    answer = ','.join(answer)
                problems[question].update({answer: bucket['count']})

            return problems
        else:
            log.error("Error fetching %s, code: %s, msg: %s",
                      url, res.status_code, res.content)
        return None

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("AnswerDistHistogramBlock",
             """<answerhisto/>"""
            )
        ]

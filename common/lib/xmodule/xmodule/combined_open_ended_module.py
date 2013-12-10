import logging
from lxml import etree

from pkg_resources import resource_string

from xmodule.raw_module import RawDescriptor
from .x_module import XModule
from xblock.fields import Integer, Scope, String, List, Float, Boolean
from xmodule.open_ended_grading_classes.combined_open_ended_modulev1 import CombinedOpenEndedV1Module, CombinedOpenEndedV1Descriptor
from collections import namedtuple
from .fields import Date, Timedelta
import textwrap

log = logging.getLogger("mitx.courseware")

V1_SETTINGS_ATTRIBUTES = [
    "display_name", "max_attempts", "graded", "accept_file_upload",
    "skip_spelling_checks", "due", "graceperiod", "weight", "min_to_calibrate",
    "max_to_calibrate", "peer_grader_count", "required_peer_grading",
]

V1_STUDENT_ATTRIBUTES = ["current_task_number", "task_states", "state",
                         "student_attempts", "ready_to_reset", "old_task_states"]

V1_ATTRIBUTES = V1_SETTINGS_ATTRIBUTES + V1_STUDENT_ATTRIBUTES

VersionTuple = namedtuple('VersionTuple', ['descriptor', 'module', 'settings_attributes', 'student_attributes'])
VERSION_TUPLES = {
    1: VersionTuple(CombinedOpenEndedV1Descriptor, CombinedOpenEndedV1Module, V1_SETTINGS_ATTRIBUTES,
                    V1_STUDENT_ATTRIBUTES),
}

DEFAULT_VERSION = 1
DEFAULT_DATA = textwrap.dedent("""\
<combinedopenended>
    <prompt>
        <h3>Censorship in the Libraries</h3>

        <p>'All of us can think of a book that we hope none of our children or any other children have taken off the shelf. But if I have the right to remove that book from the shelf -- that work I abhor -- then you also have exactly the same right and so does everyone else. And then we have no books left on the shelf for any of us.' --Katherine Paterson, Author
        </p>

        <p>
        Write a persuasive essay to a newspaper reflecting your views on censorship in libraries. Do you believe that certain materials, such as books, music, movies, magazines, etc., should be removed from the shelves if they are found offensive? Support your position with convincing arguments from your own experience, observations, and/or reading.
        </p>

    </prompt>
    <rubric>
        <rubric>
        <category>
        <description>
        Is your response ready to send to your portfolio?
        </description>
        <option>
        No
        </option>
        <option>
        Yes
        </option>

        </category>
        </rubric>
    </rubric>

    <task>
    <selfassessment/></task>
    

</combinedopenended>
""")


class VersionInteger(Integer):
    """
    A model type that converts from strings to integers when reading from json.
    Also does error checking to see if version is correct or not.
    """

    def from_json(self, value):
        try:
            value = int(value)
            if value not in VERSION_TUPLES:
                version_error_string = "Could not find version {0}, using version {1} instead"
                log.error(version_error_string.format(value, DEFAULT_VERSION))
                value = DEFAULT_VERSION
        except:
            value = DEFAULT_VERSION
        return value


class CombinedOpenEndedFields(object):
    display_name = String(
        display_name="Display Name",
        help="This name appears in the horizontal navigation at the top of the page.",
        default="Open Response Assessment",
        scope=Scope.settings
    )
    current_task_number = Integer(
        help="Current task that the student is on.",
        default=0,
        scope=Scope.user_state
    )
    old_task_states = List(
        help=("A list of lists of state dictionaries for student states that are saved."
               "This field is only populated if the instructor changes tasks after"
               "the module is created and students have attempted it (for example changes a self assessed problem to "
               "self and peer assessed."),
        scope = Scope.user_state
    )
    task_states = List(
        help="List of state dictionaries of each task within this module.",
        scope=Scope.user_state
    )
    state = String(
        help="Which step within the current task that the student is on.",
        default="initial",
        scope=Scope.user_state
    )
    graded = Boolean(
        display_name="Graded",
        help='Defines whether the student gets credit for grading this problem.',
        default=True,
        scope=Scope.settings
    )
    student_attempts = Integer(
        help="Number of attempts taken by the student on this problem",
        default=0,
        scope=Scope.user_state
    )
    ready_to_reset = Boolean(
        help="If the problem is ready to be reset or not.",
        default=False,
        scope=Scope.user_state
    )
    max_attempts = Integer(
        display_name="Maximum Attempts",
        help="The number of times the student can try to answer this problem.",
        default=99999,
        scope=Scope.settings,
        values={"min": 9999 }
    )
    accept_file_upload = Boolean(
        display_name="Allow File Uploads",
        help="Whether or not the student can submit files as a response.",
        default=False,
        scope=Scope.settings
    )
    skip_spelling_checks = Boolean(
        display_name="Disable Quality Filter",
        help="If False, the Quality Filter is enabled and submissions with poor spelling, short length, or poor grammar will not be peer reviewed.",
        default=False,
        scope=Scope.settings
    )
    due = Date(
        help="Date that this problem is due by",
        scope=Scope.settings
    )
    graceperiod = Timedelta(
        help="Amount of time after the due date that submissions will be accepted",
        scope=Scope.settings
    )
    version = VersionInteger(help="Current version number", default=DEFAULT_VERSION, scope=Scope.settings)
    data = String(help="XML data for the problem", scope=Scope.content,
        default=DEFAULT_DATA)
    weight = Float(
        display_name="Problem Weight",
        help="Defines the number of points each problem is worth. If the value is not set, each problem is worth one point.",
        scope=Scope.settings,
        values={"min": 0, "step": ".1"},
        default=1
    )
    min_to_calibrate = Integer(
        display_name="Minimum Peer Grading Calibrations",
        help="The minimum number of calibration essays each student will need to complete for peer grading.",
        default=3,
        scope=Scope.settings,
        values={"min": 1, "max": 20, "step": "1"}
    )
    max_to_calibrate = Integer(
        display_name="Maximum Peer Grading Calibrations",
        help="The maximum number of calibration essays each student will need to complete for peer grading.",
        default=6,
        scope=Scope.settings,
        values={"min": 1, "max": 20, "step": "1"}
    )
    peer_grader_count = Integer(
        display_name="Peer Graders per Response",
        help="The number of peers who will grade each submission.",
        default=3,
        scope=Scope.settings,
        values={"min": 1, "step": "1", "max": 5}
    )
    required_peer_grading = Integer(
        display_name="Required Peer Grading",
        help="The number of other students each student making a submission will have to grade.",
        default=3,
        scope=Scope.settings,
        values={"min": 1, "step": "1", "max": 5}
    )
    markdown = String(
        help="Markdown source of this module",
        default=textwrap.dedent("""\
                    [prompt]
                        <h3>Censorship in the Libraries</h3>

                        <p>'All of us can think of a book that we hope none of our children or any other children have taken off the shelf. But if I have the right to remove that book from the shelf -- that work I abhor -- then you also have exactly the same right and so does everyone else. And then we have no books left on the shelf for any of us.' --Katherine Paterson, Author
                        </p>

                        <p>
                        Write a persuasive essay to a newspaper reflecting your vies on censorship in libraries. Do you believe that certain materials, such as books, music, movies, magazines, etc., should be removed from the shelves if they are found offensive? Support your position with convincing arguments from your own experience, observations, and/or reading.
                        </p>
                    [prompt]
                    [rubric]
                    + Is your response ready to send to your portfolio?
                    - No
                    - Yes
                    [rubric]
                    [tasks]
                    (Self)
                    [tasks]

        """),
        scope=Scope.settings
    )


class CombinedOpenEndedModule(CombinedOpenEndedFields, XModule):
    """
    This is a module that encapsulates all open ended grading (self assessment, peer assessment, etc).
    It transitions between problems, and support arbitrary ordering.
    Each combined open ended module contains one or multiple "child" modules.
    Child modules track their own state, and can transition between states.  They also implement get_html and
    handle_ajax.
    The combined open ended module transitions between child modules as appropriate, tracks its own state, and passess
    ajax requests from the browser to the child module or handles them itself (in the cases of reset and next problem)
    ajax actions implemented by all children are:
        'save_answer' -- Saves the student answer
        'save_assessment' -- Saves the student assessment (or external grader assessment)
        'save_post_assessment' -- saves a post assessment (hint, feedback on feedback, etc)
    ajax actions implemented by combined open ended module are:
        'reset' -- resets the whole combined open ended module and returns to the first child module
        'next_problem' -- moves to the next child module
        'get_results' -- gets results from a given child module

    Types of children. Task is synonymous with child module, so each combined open ended module
    incorporates multiple children (tasks):
        openendedmodule
        selfassessmentmodule

    CombinedOpenEndedModule.__init__ takes the same arguments as xmodule.x_module:XModule.__init__
    """
    STATE_VERSION = 1

    # states
    INITIAL = 'initial'
    ASSESSING = 'assessing'
    INTERMEDIATE_DONE = 'intermediate_done'
    DONE = 'done'

    icon_class = 'problem'

    js = {
            'coffee':
            [
                resource_string(__name__, 'js/src/combinedopenended/display.coffee'),
                resource_string(__name__, 'js/src/collapsible.coffee'),
                resource_string(__name__, 'js/src/javascript_loader.coffee'),
            ]
    }
    js_module_name = "CombinedOpenEnded"

    css = {'scss': [resource_string(__name__, 'css/combinedopenended/display.scss')]}

    def __init__(self, *args, **kwargs):
        """
        Definition file should have one or many task blocks, a rubric block, and a prompt block.

        See DEFAULT_DATA for a sample.

        """
        XModule.__init__(self, *args, **kwargs)

        self.system.set('location', self.location)

        if self.task_states is None:
            self.task_states = []

        if self.old_task_states is None:
            self.old_task_states = []

        version_tuple = VERSION_TUPLES[self.version]

        self.student_attributes = version_tuple.student_attributes
        self.settings_attributes = version_tuple.settings_attributes

        attributes = self.student_attributes + self.settings_attributes

        static_data = {}
        instance_state = {k: getattr(self, k) for k in attributes}
        self.child_descriptor = version_tuple.descriptor(self.system)
        self.child_definition = version_tuple.descriptor.definition_from_xml(etree.fromstring(self.data), self.system)
        self.child_module = version_tuple.module(self.system, self.location, self.child_definition, self.child_descriptor,
                                                 instance_state=instance_state, static_data=static_data,
                                                 attributes=attributes)
        self.save_instance_data()

    def get_html(self):
        self.save_instance_data()
        return_value = self.child_module.get_html()
        return return_value

    def handle_ajax(self, dispatch, data):
        self.save_instance_data()
        return_value = self.child_module.handle_ajax(dispatch, data)
        self.save_instance_data()
        return return_value

    def get_instance_state(self):
        return self.child_module.get_instance_state()

    def get_score(self):
        return self.child_module.get_score()

    def max_score(self):
        return self.child_module.max_score()

    def get_progress(self):
        return self.child_module.get_progress()

    @property
    def due_date(self):
        return self.child_module.due_date

    def save_instance_data(self):
        for attribute in self.student_attributes:
            setattr(self, attribute, getattr(self.child_module, attribute))


class CombinedOpenEndedDescriptor(CombinedOpenEndedFields, RawDescriptor):
    """
    Module for adding combined open ended questions
    """
    mako_template = "widgets/open-ended-edit.html"
    module_class = CombinedOpenEndedModule

    has_score = True
    always_recalculate_grades = True
    template_dir_name = "combinedopenended"

    #Specify whether or not to pass in S3 interface
    needs_s3_interface = True

    #Specify whether or not to pass in open ended interface
    needs_open_ended_interface = True

    metadata_attributes = RawDescriptor.metadata_attributes

    js = {'coffee': [resource_string(__name__, 'js/src/combinedopenended/edit.coffee')]}
    js_module_name = "OpenEndedMarkdownEditingDescriptor"
    css = {'scss': [resource_string(__name__, 'css/editor/edit.scss'), resource_string(__name__, 'css/combinedopenended/edit.scss')]}

    metadata_translations = {
        'is_graded': 'graded',
        'attempts': 'max_attempts',
        }

    def get_context(self):
        _context = RawDescriptor.get_context(self)
        _context.update({'markdown': self.markdown,
                         'enable_markdown': self.markdown is not None})
        return _context

    @property
    def non_editable_metadata_fields(self):
        non_editable_fields = super(CombinedOpenEndedDescriptor, self).non_editable_metadata_fields
        non_editable_fields.extend([CombinedOpenEndedDescriptor.due, CombinedOpenEndedDescriptor.graceperiod,
                                    CombinedOpenEndedDescriptor.markdown, CombinedOpenEndedDescriptor.version])
        return non_editable_fields

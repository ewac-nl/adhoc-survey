# coding: utf-8
# © 2015 ADHOC SA (http://www.adhoc.com.ar)
# © 2020 Opener B.V. (https://opener.amsterdam)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    @api.model
    def get_hidden_questions(self):
        """ Return the questions that should be hidden based on the current
        user input """
        questions_to_hide = self.env['survey.question']
        questions = self.survey_id.mapped('page_ids.question_ids')
        for question in questions.filtered('is_conditional'):
            for question2 in questions.filtered(
                    lambda x: x == question.triggering_question_id):
                input_answer_ids = self.user_input_line_ids.filtered(
                    lambda x: x.question_id == question2)
                if question.triggering_answer_id not in (
                        input_answer_ids.mapped('value_suggested')):
                    questions_to_hide += question
        return questions_to_hide

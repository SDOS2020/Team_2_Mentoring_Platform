const DisplaySummary = {
	delimiters: ["[[", "]]"],
	template: `
	<div>
		<button style="background-color: #7474aa; color: white;" class="btn btn-block" data-toggle="modal" :data-target="'#viewSummaryModal' + meeting_id" data-whatever="@mdo">
			Show summary
		</button>

		<div class="modal fade" :id="'viewSummaryModal' + meeting_id" tabindex="-1" role="dialog" aria-labelledby="'viewSummaryModalLabel' + meeting_id" aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content">

					<div class="modal-header">
						<h5 class="modal-title" id="'viewSummaryModalLabel' + meeting_id">
							Summary of the meeting
						</h5>
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>

					<div class="modal-body">
						<table class="table">
							<tr>
								<th>Meeting date</th>
								<td style="width: 70%;">[[ meeting_date ]]</td>
							</tr>

							<tr>
								<th>Meeting duration</th>
								<td style="width: 70%;">[[meeting_length]]</td>
							</tr>
							<tr>
								<th>Meeting details</th>
								<td style="width: 70%;">[[meeting_details]]</td>
							</tr>
							<tr>
								<th>Action items</th>
								<td style="width: 70%;">[[meeting_todos]]</td>
							</tr>
							<tr>
								<th>Next meeting date</th>
								<td style="width: 70%;">[[next_meeting_date]]</td>
							</tr>
							<tr>
								<th>Next meeting agenda</th>
								<td style="width: 70%;">[[next_meeting_agenda]]</td>
							</tr>
						</table>
					</div>

					<div class="modal-footer">
						<button class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>
				</div>
			</div>
		</div>
	</div>
	`,
	props: {
		meeting_id: {required: true},
		meeting_date: {required: true},
		meeting_length: {required: true},
		meeting_details: {required: true},
		meeting_todos: {required: true},
		next_meeting_date: {required: true},
		next_meeting_agenda: {required: true},
	}
};

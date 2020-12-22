const AddMeetingSummary = {
	delimiters: ["[[", "]]"],
	template: `
	<div>
		<center>
			<button style="background-color: #7474aa; color: white;" class="btn btn-block" data-toggle="modal" data-target="#addSummaryModal" data-whatever="@mdo">
				Add meeting summary
			</button>
		</center>

		<div class="modal fade" id="addSummaryModal" tabindex="-1" role="dialog" aria-labelledby="addSummaryModalLabel" aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content">

					<div class="modal-header">
						<h5 class="modal-title" id="addSummaryModalLabel">
							Add summary of the meeting
						</h5>
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>

					<div class="modal-body">
						<form>
							<div class="form-group">
								<label class="col-form-label">Start time:</label>
								<br/>
								<input v-model="meeting_date" type="datetime-local" min="2020-12-22T08:30" required>
							</div>
						
							<div class="form-group">
								<label class="col-form-label">Meeting duration (hrs):</label>
								<input v-model="meeting_length" type="text" class="form-control">
							</div>

							<div class="form-group">
								<label class="col-form-label">Meeting details:</label>
								<textarea v-model="meeting_details" class="form-control"></textarea>
							</div>

							<div class="form-group">
								<label class="col-form-label">Action items:</label>
								<textarea v-model="meeting_todos" class="form-control"></textarea>
							</div>
							
							<div class="form-group">
								<label class="col-form-label">Next meeting date:</label>
								<br/>
								<input v-model="next_meeting_date" type="datetime-local" min="2020-12-22T08:30" required>
							</div>
							
							<div class="form-group">
								<label class="col-form-label">Next meeting agenda:</label>
								<textarea v-model="next_meeting_agenda" class="form-control"></textarea>
							</div>
						</form>
					</div>


					<div class="modal-footer">
						<button v-on:click="add_new_meeting" class="btn btn-success">Add Summary</button>
						<button id="summary-close-button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>
				</div>
			</div>
		</div>
	</div>
	`,
	
	data() {
		return {
			meeting_date: "",
			meeting_length: "",
			meeting_details: "",
			meeting_todos: "",
			next_meeting_date: "",
			next_meeting_agenda: "",
		};
	},

	props: {
		guest_name: {
			required: true
		},
		csrf: {
			required: true
		},
	},

	methods: {
		validate_input() {
			let alert_message = "";
			if (this.meeting_details.length === 0) {
				alert_message += "Please fill the meeting details\n";
			}

			if (alert_message.length === 0) {
				alert("Summary successfully added!")
				return true;
			}
			else {
				alert("[ERROR]\n" + alert_message);
				return false;
			}
		},

		add_new_meeting() {
			if (!this.validate_input()) {
				return;
			}

			let request_url = "http://127.0.0.1:8000/api/add_meeting_summary/";

			axios.post(request_url, {
				'guest_name': this.guest_name,
				'meeting_date': this.meeting_date,
				'meeting_length': this.meeting_length,
				'meeting_details': this.meeting_details,
				'meeting_todos': this.meeting_todos,
				'next_meeting_date': this.next_meeting_date,
				'next_meeting_agenda': this.next_meeting_agenda,
			}, {
				headers: {
					'X-CSRFTOKEN': this.csrf
				}
			})
			.then(response => {
			})
			.catch(error => {
				console.log('[ERROR]');
				console.log(error);
			});

			this.meeting_date = "";
			this.meeting_length = "";
			this.meeting_details = "";
			this.meeting_todos = "";
			this.next_meeting_date = "";
			this.next_meeting_agenda = "";

			document.getElementById("summary-close-button").click();
		}
	}
};

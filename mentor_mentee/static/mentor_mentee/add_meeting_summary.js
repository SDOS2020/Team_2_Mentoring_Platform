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
		limit_content_size(content, lower, upper, type) {
			if (content.length < lower) {
				alert('[ERROR] Please elaborate on ' + type);
				return false;
			}

			if (content.length > upper) {
				alert('[ERROR] Please shorten the content of ' + type);
				return false;
			}

			return true;
		},

		add_new_meeting() {
			if (!this.limit_content_size(this.meeting_date, 4, 100, 'Meeting Date')) { return; }
			if (!this.limit_content_size(this.meeting_details, 8, 512, 'Meeting Details')) { return; }
			if (!this.limit_content_size(this.next_meeting_date, 4, 100, 'Next Meeting Date')) { return; }
			if (!this.limit_content_size(this.next_meeting_agenda, 0, 512, 'Next Meeting Agenda')) { return; }

			let today = new Date();
			let sd = new Date(this.meeting_date);
			if (sd > today) {
				alert('[ERROR] Invalid start time');
				return ;
			}

			let nmd = new Date(this.next_meeting_date);
			if (nmd < sd) {
				alert('[ERROR] Next meeting date cannot be less than start time');
				return;
			}

			let request_url = "/api/add_meeting_summary/";

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

			alert('[SUCCESS] Meeting summary added');
			document.getElementById("summary-close-button").click();
		}
	}
};

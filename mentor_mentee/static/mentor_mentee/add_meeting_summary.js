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
								<input v-model="meeting_date" id="start-time" type="datetime-local" class="form-control" max="" required>
							</div>
						
							<div class="form-group">
								<label class="col-form-label">Meeting duration (hrs):</label>
								<input v-model="meeting_length" type="number" step="0.01" min="0" class="form-control">
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
								<input v-model="next_meeting_date" type="datetime-local" class="form-control" required>
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

	mounted() {
		var today = new Date();
		var dd = today.getDate();
		var mm = today.getMonth()+1; //January is 0!
		var yyyy = today.getFullYear();
		if (dd < 10) {
				dd ='0'+ dd
		}

		if (mm < 10) {
			mm = '0' + mm
		} 

		today = yyyy + '-' + mm + '-' + dd + 'T23:59:59';
	
		document.getElementById("start-time").setAttribute("max", today);
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

			try {
				this.meeting_length = parseFloat(this.meeting_length);
				if (this.meeting_length <= 0) {
					alert('[ERROR] Meeting length cannot be <= 0');
					return;
				}
			}
			catch(error) {
				alert('[ERROR] Invalid input for meeting length');
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

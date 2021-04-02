const ScheduleMeeting = {
	delimiters: ["[[", "]]"],
	template: `
	<div>
		<center>
			<button style="background-color: #7474aa; color: white;" class="btn btn-block" data-toggle="modal" data-target="#scheduleModal" data-whatever="@mdo">
				Schedule a meeting &nbsp
				<i class="fas fa-calendar-plus"></i>
			</button>
		</center>
	
		<div class="modal fade" id="scheduleModal" tabindex="-1" role="dialog" aria-labelledby="scheduleModalLabel" aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content">


					<div class="modal-header">
						<h5 class="modal-title" id="scheduleModalLabel">Schedule a meeting</h5>
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>


					<div class="modal-body">
						<form>
							<div class="form-group">
								<label for="meeting-title" class="col-form-label">Title:</label>
								<input v-model="meeting_title" type="text" class="form-control" id="meeting-title">
							</div>

							<div class="form-group">
								<label for="message-agenda" class="col-form-label">Agenda:</label>
								<textarea v-model="meeting_agenda" class="form-control" id="message-agenda"></textarea>
							</div>

							<div class="form-group">
								<label for="meeting-url" class="col-form-label">Meeting URL:</label>
								<input v-model="meeting_url" type="text" class="form-control" id="meeting-url">
							</div>
								
							<div class="form-group">
								<label for="meeting-time" class="col-form-label">Time:</label>
								<br/>
								<input v-model="meeting_time" type="datetime-local" class="form-control" id="meeting-time" name="meeting-time" min="2020-11-20T08:30" required>
							</div>
						</form>
					</div>


					<div class="modal-footer">
						<button v-on:click="add_new_meeting" class="btn btn-success">Schedule</button>
						<button id="close-button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					</div>
				</div>
			</div>
		</div>
	</div>
	`,
	data() {
		return {
			meeting_title: "",
			meeting_agenda: "",
			meeting_url: "",
			meeting_time: "",
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
			if (this.meeting_title.length === 0) {
				alert_message += "Please fill the title\n";
			}

			if (this.meeting_time.length === 0) {
				alert_message += "Please fill the time\n";
			}

			if (alert_message.length === 0) {
				alert("[SUCCESS]\nMeeting successfully scheduled!")
				return true;
			}
			else {
				alert("[ERROR]\n" + alert_message);
				return false;
			}
		},

		add_new_meeting() {
			if (!this.validate_input()) {
				return ;
			}

			let request_url = "/api/add_meeting/";

			axios.post(request_url, {
				'guest_name': this.guest_name,
				'title': this.meeting_title,
				'agenda': this.meeting_agenda,
				'meeting_url': this.meeting_url,
				'time': this.meeting_time,
			}, {
				headers: {
					'X-CSRFTOKEN': this.csrf
				}
			})
			.then(response => {
				
				this.meeting_title = "";
				this.meeting_agenda = "";
				this.meeting_url = "";
				this.meeting_time = "";

				// document.getElementById("close-button").click();
				$('#scheduleModal').modal('hide');
				$('body').removeClass('modal-open');
				$('.modal-backdrop').remove();
				
				location.reload();
			})
			.catch(error => {
				console.log('[ERROR]');
				console.log(error);
				this.meeting_title = "";
				this.meeting_agenda = "";
				this.meeting_url = "";
				this.meeting_time = "";

				// document.getElementById("close-button").click();
				$('#scheduleModal').modal('hide');
				$('body').removeClass('modal-open');
				$('.modal-backdrop').remove();
			});
		}
	}
};

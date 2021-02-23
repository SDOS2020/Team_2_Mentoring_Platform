const ShowMeeting = {
	delimiters: ["[[", "]]"],
	template: `
	<div>
		<div class="card-header" style="border-radius: 10px 10px 0 0; background-color: lightgrey;" id="show-meetings-header">
			<center>
				<font size="4">
					<b>Upcoming Meetings</b>
				</font>
			</center>
		</div>

		<div style="height: 30vh; overflow-y: scroll;" id="show-meetings-body">
			<div v-if="meetings.length === 0" id="no-meetings-text">
				<center style="margin-top: 5rem;">
					No scheduled meetings
				</center>
			</div>

			<table class="table table-hover table-striped">
				<tbody>
					<tr v-for="(meeting, index) in meetings">
						<td>
							<b>[[ meeting.time ]]</b>
							<br/>
							<i>
								<small class="text-muted">
									[[ meeting.date ]], [[ meeting.day ]]
								</small>
							</i>
						</td>

						<td style="width: 60%; padding-right: 0; padding-left: 0;">
							<a v-bind:href="meeting.meeting_url" target="blank" style="text-decoration: none; color: black;">
								<b>[[ meeting.title ]]</b> &nbsp
								
								<a v-bind:href="meeting.meeting_url" target="blank">
									<i class="fas fa-video"></i>
								</a>
								
								<br/>
								<small class="text-muted">[[ meeting.agenda ]]</small>
							</a>
						</td>

						<td style="width: 10%;">
							<button 
								style="background-color: #7474aa; color: white;" 
								class="btn btn-sm btn-block" 
								data-toggle="modal" 
								:data-target="'#editMeetModal' + index" 
								data-whatever="@mdo"
							>
								Edit
							</button>
						</td>

						<div class="modal fade" :id="'editMeetModal' + index" tabindex="-1" role="dialog" :aria-labelledby="'editMeetModalLabel' + index" aria-hidden="true">
							<div class="modal-dialog" role="document">
								<div class="modal-content">

									<div class="modal-header">
										<h5 class="modal-title" :id="'editMeetModalLabel' + index">Edit meeting</h5>
										<button type="button" class="close" data-dismiss="modal" aria-label="Close">
											<span aria-hidden="true">&times;</span>
										</button>
									</div>

									<div class="modal-body">
										<form>
											<div class="form-group">
												<label for="meeting-title" class="col-form-label">Title:</label>
												<input v-model="meeting.title" type="text" class="form-control" id="meeting-title">
											</div>

											<div class="form-group">
												<label for="message-agenda" class="col-form-label">Agenda:</label>
												<textarea v-model="meeting.agenda" class="form-control" id="message-agenda"></textarea>
											</div>

											<div class="form-group">
												<label for="meeting-url" class="col-form-label">Meeting URL:</label>
												<input v-model="meeting.meeting_url" type="text" class="form-control" id="meeting-url">
											</div>
												
											<div class="form-group">
												<label for="meeting-time" class="col-form-label">Time:</label>
												<br/>
												<input v-model="m_time" type="datetime-local" class="form-control" id="meeting-time" name="meeting-time" min="2020-11-20T08:30" required>
											</div>
										</form>
									</div>

									<div class="modal-footer">
										<button v-on:click="edit_meeting(index)" class="btn btn-success">Confirm changes</button>
										<button id="close-button" class="btn btn-secondary" data-dismiss="modal">Close</button>
									</div>
								</div>
							</div>
						</div>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
	`,
	data() {
		return {
			meetings: [],
			m_time: "",
		};
	},

	props: {
		guest_name: null,
		csrf: {
			required: true
		},
	},
	
	created() {
		// TO TEST MENTOR STATISTICS
		// let request_url = "/api/get_mentor_statistics/";
		// axios.get(request_url, {
		// 	params: {
		// 		'mentor_username': 'shaurya',
		// 		'n_active_mentees': '',
		// 		'n_total_mentees': '',
		// 		'n_rejected_mentees': '',
		// 		'n_meetings': '',
		// 		'n_messages_sent': '',
		// 		'n_messages_received': '',
		// 		'responsibilities': '',
		// 		'will_mentor': '',
		// 	}
		// })
		// .then(response => {
		// 	console.log(response.data);
		// })
		// .catch(error => {
		// 	console.log('[ERROR]');
		// });

		// TO TEST MENTOR-MENTEE STATISTICS
		// let request_url = "/api/get_mentor_mentee_statistics/";
		// axios.get(request_url, {
		// 	params: {
		// 		'mentor_username': 'shaurya',
		// 		'mentee_username': 'pratik',
		// 		'n_meetings': '',
		// 		'n_messages': '',
		// 		'n_meeting_summaries': '',
		// 		'n_milestones': '',
		// 		'avg_meeting_duration': '',
		// 	}
		// })
		// .then(response => {
		// 	console.log(response.data);
		// })
		// .catch(error => {
		// 	console.log('[ERROR]');
		// });

		this.get_meetings();
		// window.setInterval(this.get_meetings, 1000);
	},

	methods: {
		get_meetings() {
			let request_url = "/api/get_meetings/" + this.guest_name;

			axios.get(request_url)
			.then(response => {
				this.meetings = response.data.meetings;
			})
			.catch(error => {
				console.log('[ERROR]');
				console.log(error);
			});
		},
		edit_meeting(index) {
			let request_url = "/api/edit_meeting/";

			axios.post(request_url, {
				'id': this.meetings[index].id,
				'title': this.meetings[index].title,
				'agenda': this.meetings[index].agenda,
				'meeting_url': this.meetings[index].meeting_url,
				'time': this.m_time,
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
			
			$('#editMeetModal' + index).modal('hide');

			$('body').removeClass('modal-open');
			$('.modal-backdrop').remove();

			this.get_meetings();
		}
	}
};

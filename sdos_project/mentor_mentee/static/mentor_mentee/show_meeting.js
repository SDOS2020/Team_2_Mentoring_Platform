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
					<tr v-for="meeting in meetings">
						<td>
							<b>[[ meeting.time ]]</b>
							<br/>
							<i>
								<small class="text-muted">
									[[ meeting.date ]], [[ meeting.day ]]
								</small>
							</i>
						</td>

						<td style="width: 75%;">
							<a v-bind:href="meeting.meeting_url" target="blank" style="text-decoration: none; color: black;">
								<b>[[ meeting.title ]]</b> &nbsp
								
								<a v-bind:href="meeting.meeting_url" target="blank">
									<i class="fas fa-video"></i>
								</a>
								
								<br/>
								<small class="text-muted">[[ meeting.agenda ]]</small>
							</a>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
	`,
	data() {
		return {
			meetings: [],
		};
	},

	props: {
		guest_name: null,
	},

	created() {
		this.get_meetings();
		window.setInterval(this.get_meetings, 1000);
	},

	methods: {
		get_meetings() {
			let request_url = "http://127.0.0.1:8000/api/get_meetings/" + this.guest_name;

			axios.get(request_url)
			.then(response => {
				this.meetings = response.data.meetings;
			})
			.catch(error => {
				console.log('[ERROR]');
				console.log(error);
			});
		}
	}
};

const ShowMeetingSummary = {
	delimiters: ["[[", "]]"],
	components: {
		"display-summary": DisplaySummary
	},
	template: `
	<div>
		<div class="card-header" style="border-radius: 10px 10px 0 0; background-color: lightgrey;" id="show-summary-header">
			<center>
				<font size="4">
					<b>Past Meeting Details</b>
				</font>
			</center>
		</div>

		<div style="height: 30vh; overflow-y: scroll;" id="show-summary-body">
			<div v-if="summaries.length === 0" id="no-meetings-text">
				<center style="margin-top: 5rem;">
					No past meeting summaries
				</center>
			</div>

			<table class="table table-hover table-striped">
				<tbody>
					<tr v-for="(summary, index) in summaries">
						<td>
							<b>[[ summary.time ]]</b>
							<br/>
							<i>
								<small class="text-muted">
									[[ summary.date ]], [[ summary.day ]]
								</small>
							</i>
						</td>

						<td style="width: 75%;">
							<display-summary
								:meeting_id="index"
								:meeting_date="summary.meeting_date"
								:meeting_length="summary.meeting_length"
								:meeting_details="summary.meeting_details"
								:meeting_todos="summary.meeting_todos"
								:next_meeting_date="summary.next_meeting_date"
								:next_meeting_agenda="summary.next_meeting_agenda"
							>
							</display-summary>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
	`,
	data() {
		return {
			summaries: [],
		};
	},

	props: {
		guest_name: null,
	},

	created() {
		this.get_meeting_summaries();
		window.setInterval(this.get_meeting_summaries, 2000);
	},

	methods: {
		get_meeting_summaries() {
			let request_url = "http://127.0.0.1:8000/api/get_meeting_summaries/" + this.guest_name;

			axios.get(request_url)
			.then(response => {
				this.summaries = response.data.summaries;
			})
			.catch(error => {
				console.log('[ERROR]');
				console.log(error);
			});
		}
	}
};

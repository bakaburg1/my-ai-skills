// Copyright (c) 2026 Angelo D'Ambrosio
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Text.RegularExpressions;
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;
using OpenXmlPowerTools;

internal static class Program
{
	private record StatusOut(bool hasTrackedChanges, bool hasComments, string commentModel, LengthOut estimatedLength)
	{
		[CompilerGenerated]
		protected virtual global::System.Type EqualityContract
		{
			[CompilerGenerated]
			get
			{
				return typeof(StatusOut);
			}
		}

		[CompilerGenerated]
		public override string ToString()
		{
			//IL_0000: Unknown result type (might be due to invalid IL or missing references)
			//IL_0006: Expected O, but got Unknown
			StringBuilder val = new StringBuilder();
			val.Append("StatusOut");
			val.Append(" { ");
			if (PrintMembers(val))
			{
				val.Append(' ');
			}
			val.Append('}');
			return ((object)val).ToString();
		}

		[CompilerGenerated]
		protected virtual bool PrintMembers(StringBuilder builder)
		{
			RuntimeHelpers.EnsureSufficientExecutionStack();
			builder.Append("hasTrackedChanges = ");
			builder.Append(((object)hasTrackedChanges/*cast due to constrained. prefix*/).ToString());
			builder.Append(", hasComments = ");
			builder.Append(((object)hasComments/*cast due to constrained. prefix*/).ToString());
			builder.Append(", commentModel = ");
			builder.Append((object)commentModel);
			builder.Append(", estimatedLength = ");
			builder.Append((object)estimatedLength);
			return true;
		}

		[CompilerGenerated]
		public virtual bool Equals(StatusOut? other)
		{
			if ((object)this != other)
			{
				if ((object)other != null && EqualityContract == other.EqualityContract && EqualityComparer<bool>.Default.Equals(hasTrackedChanges, other.hasTrackedChanges) && EqualityComparer<bool>.Default.Equals(hasComments, other.hasComments) && EqualityComparer<string>.Default.Equals(commentModel, other.commentModel))
				{
					return EqualityComparer<LengthOut>.Default.Equals(estimatedLength, other.estimatedLength);
				}
				return false;
			}
			return true;
		}
	}

	private record LengthOut(int paragraphs, int headings)
	{
		[CompilerGenerated]
		protected virtual global::System.Type EqualityContract
		{
			[CompilerGenerated]
			get
			{
				return typeof(LengthOut);
			}
		}

		[CompilerGenerated]
		public override string ToString()
		{
			//IL_0000: Unknown result type (might be due to invalid IL or missing references)
			//IL_0006: Expected O, but got Unknown
			StringBuilder val = new StringBuilder();
			val.Append("LengthOut");
			val.Append(" { ");
			if (PrintMembers(val))
			{
				val.Append(' ');
			}
			val.Append('}');
			return ((object)val).ToString();
		}

		[CompilerGenerated]
		protected virtual bool PrintMembers(StringBuilder builder)
		{
			RuntimeHelpers.EnsureSufficientExecutionStack();
			builder.Append("paragraphs = ");
			builder.Append(((object)paragraphs/*cast due to constrained. prefix*/).ToString());
			builder.Append(", headings = ");
			builder.Append(((object)headings/*cast due to constrained. prefix*/).ToString());
			return true;
		}

		[CompilerGenerated]
		public virtual bool Equals(LengthOut? other)
		{
			if ((object)this != other)
			{
				if ((object)other != null && EqualityContract == other.EqualityContract && EqualityComparer<int>.Default.Equals(paragraphs, other.paragraphs))
				{
					return EqualityComparer<int>.Default.Equals(headings, other.headings);
				}
				return false;
			}
			return true;
		}
	}

	private record OutlineItem(int index, string paraId, int level, string text)
	{
		[CompilerGenerated]
		protected virtual global::System.Type EqualityContract
		{
			[CompilerGenerated]
			get
			{
				return typeof(OutlineItem);
			}
		}

		[CompilerGenerated]
		public override string ToString()
		{
			//IL_0000: Unknown result type (might be due to invalid IL or missing references)
			//IL_0006: Expected O, but got Unknown
			StringBuilder val = new StringBuilder();
			val.Append("OutlineItem");
			val.Append(" { ");
			if (PrintMembers(val))
			{
				val.Append(' ');
			}
			val.Append('}');
			return ((object)val).ToString();
		}

		[CompilerGenerated]
		protected virtual bool PrintMembers(StringBuilder builder)
		{
			RuntimeHelpers.EnsureSufficientExecutionStack();
			builder.Append("index = ");
			builder.Append(((object)index/*cast due to constrained. prefix*/).ToString());
			builder.Append(", paraId = ");
			builder.Append((object)paraId);
			builder.Append(", level = ");
			builder.Append(((object)level/*cast due to constrained. prefix*/).ToString());
			builder.Append(", text = ");
			builder.Append((object)text);
			return true;
		}

		[CompilerGenerated]
		public virtual bool Equals(OutlineItem? other)
		{
			if ((object)this != other)
			{
				if ((object)other != null && EqualityContract == other.EqualityContract && EqualityComparer<int>.Default.Equals(index, other.index) && EqualityComparer<string>.Default.Equals(paraId, other.paraId) && EqualityComparer<int>.Default.Equals(level, other.level))
				{
					return EqualityComparer<string>.Default.Equals(text, other.text);
				}
				return false;
			}
			return true;
		}
	}

	private record FindHit(int index, string paraId, int start, int end, string match, string context)
	{
		[CompilerGenerated]
		protected virtual global::System.Type EqualityContract
		{
			[CompilerGenerated]
			get
			{
				return typeof(FindHit);
			}
		}

		[CompilerGenerated]
		public override string ToString()
		{
			//IL_0000: Unknown result type (might be due to invalid IL or missing references)
			//IL_0006: Expected O, but got Unknown
			StringBuilder val = new StringBuilder();
			val.Append("FindHit");
			val.Append(" { ");
			if (PrintMembers(val))
			{
				val.Append(' ');
			}
			val.Append('}');
			return ((object)val).ToString();
		}

		[CompilerGenerated]
		protected virtual bool PrintMembers(StringBuilder builder)
		{
			RuntimeHelpers.EnsureSufficientExecutionStack();
			builder.Append("index = ");
			builder.Append(((object)index/*cast due to constrained. prefix*/).ToString());
			builder.Append(", paraId = ");
			builder.Append((object)paraId);
			builder.Append(", start = ");
			builder.Append(((object)start/*cast due to constrained. prefix*/).ToString());
			builder.Append(", end = ");
			builder.Append(((object)end/*cast due to constrained. prefix*/).ToString());
			builder.Append(", match = ");
			builder.Append((object)match);
			builder.Append(", context = ");
			builder.Append((object)context);
			return true;
		}

		[CompilerGenerated]
		public virtual bool Equals(FindHit? other)
		{
			if ((object)this != other)
			{
				if ((object)other != null && EqualityContract == other.EqualityContract && EqualityComparer<int>.Default.Equals(index, other.index) && EqualityComparer<string>.Default.Equals(paraId, other.paraId) && EqualityComparer<int>.Default.Equals(start, other.start) && EqualityComparer<int>.Default.Equals(end, other.end) && EqualityComparer<string>.Default.Equals(match, other.match))
				{
					return EqualityComparer<string>.Default.Equals(context, other.context);
				}
				return false;
			}
			return true;
		}
	}

	private record Anchor(string paraId, int? start, int? end)
	{
		[CompilerGenerated]
		protected virtual global::System.Type EqualityContract
		{
			[CompilerGenerated]
			get
			{
				return typeof(Anchor);
			}
		}

		[CompilerGenerated]
		public override string ToString()
		{
			//IL_0000: Unknown result type (might be due to invalid IL or missing references)
			//IL_0006: Expected O, but got Unknown
			StringBuilder val = new StringBuilder();
			val.Append("Anchor");
			val.Append(" { ");
			if (PrintMembers(val))
			{
				val.Append(' ');
			}
			val.Append('}');
			return ((object)val).ToString();
		}

		[CompilerGenerated]
		protected virtual bool PrintMembers(StringBuilder builder)
		{
			RuntimeHelpers.EnsureSufficientExecutionStack();
			builder.Append("paraId = ");
			builder.Append((object)paraId);
			builder.Append(", start = ");
			builder.Append(((object)start/*cast due to constrained. prefix*/).ToString());
			builder.Append(", end = ");
			builder.Append(((object)end/*cast due to constrained. prefix*/).ToString());
			return true;
		}

		[CompilerGenerated]
		public virtual bool Equals(Anchor? other)
		{
			if ((object)this != other)
			{
				if ((object)other != null && EqualityContract == other.EqualityContract && EqualityComparer<string>.Default.Equals(paraId, other.paraId) && EqualityComparer<int?>.Default.Equals(start, other.start))
				{
					return EqualityComparer<int?>.Default.Equals(end, other.end);
				}
				return false;
			}
			return true;
		}
	}

	private record CommentOut(string id, string? author, string? initials, string? date, string text)
	{
		[CompilerGenerated]
		protected virtual global::System.Type EqualityContract
		{
			[CompilerGenerated]
			get
			{
				return typeof(CommentOut);
			}
		}

		[CompilerGenerated]
		public override string ToString()
		{
			//IL_0000: Unknown result type (might be due to invalid IL or missing references)
			//IL_0006: Expected O, but got Unknown
			StringBuilder val = new StringBuilder();
			val.Append("CommentOut");
			val.Append(" { ");
			if (PrintMembers(val))
			{
				val.Append(' ');
			}
			val.Append('}');
			return ((object)val).ToString();
		}

		[CompilerGenerated]
		protected virtual bool PrintMembers(StringBuilder builder)
		{
			RuntimeHelpers.EnsureSufficientExecutionStack();
			builder.Append("id = ");
			builder.Append((object)id);
			builder.Append(", author = ");
			builder.Append((object)author);
			builder.Append(", initials = ");
			builder.Append((object)initials);
			builder.Append(", date = ");
			builder.Append((object)date);
			builder.Append(", text = ");
			builder.Append((object)text);
			return true;
		}

		[CompilerGenerated]
		public virtual bool Equals(CommentOut? other)
		{
			if ((object)this != other)
			{
				if ((object)other != null && EqualityContract == other.EqualityContract && EqualityComparer<string>.Default.Equals(id, other.id) && EqualityComparer<string>.Default.Equals(author, other.author) && EqualityComparer<string>.Default.Equals(initials, other.initials) && EqualityComparer<string>.Default.Equals(date, other.date))
				{
					return EqualityComparer<string>.Default.Equals(text, other.text);
				}
				return false;
			}
			return true;
		}
	}

	private static int Main(string[] args)
	{
		try
		{
			bool flag = args.Length == 0;
			if (!flag)
			{
				string text = args[0];
				bool flag2 = ((text == "-h" || text == "--help") ? true : false);
				flag = flag2;
			}
			if (flag)
			{
				PrintHelp();
				return 0;
			}
			string text2 = args[0];
			string[] args2 = Enumerable.ToArray<string>(Enumerable.Skip<string>((global::System.Collections.Generic.IEnumerable<string>)args, 1));
			if (text2 == null)
			{
				goto IL_016c;
			}
			switch (text2.Length)
			{
			case 7:
				break;
			case 6:
				goto IL_00b4;
			case 4:
				goto IL_0108;
			case 8:
				goto IL_0117;
			default:
				goto IL_016c;
			}
			char c = text2[0];
			int result;
			if ((uint)c <= 105u)
			{
				if (c != 'e')
				{
					if (c != 'i' || !(text2 == "inspect"))
					{
						goto IL_016c;
					}
					result = CmdInspect(args2);
				}
				else
				{
					if (!(text2 == "extract"))
					{
						goto IL_016c;
					}
					result = CmdExtract(args2);
				}
			}
			else if (c != 'o')
			{
				if (c != 'r' || !(text2 == "redline"))
				{
					goto IL_016c;
				}
				result = CmdRedline(args2);
			}
			else
			{
				if (!(text2 == "outline"))
				{
					goto IL_016c;
				}
				result = CmdOutline(args2);
			}
			goto IL_017e;
			IL_016c:
			result = Fail("Unknown command: " + text2);
			goto IL_017e;
			IL_017e:
			return result;
			IL_00b4:
			if (!(text2 == "status"))
			{
				goto IL_016c;
			}
			result = CmdStatus(args2);
			goto IL_017e;
			IL_0108:
			if (!(text2 == "find"))
			{
				goto IL_016c;
			}
			result = CmdFind(args2);
			goto IL_017e;
			IL_0117:
			if (!(text2 == "comments"))
			{
				goto IL_016c;
			}
			result = CmdComments(args2);
			goto IL_017e;
		}
		catch (global::System.Exception ex)
		{
			Console.Error.WriteLine(((object)ex).ToString());
			return 1;
		}
	}

	private static void PrintHelp()
	{
		Console.WriteLine("\ndocxctl (v0.1) - offline .docx inspector + navigation + redline + comments\n\nCommands:\n  status   --in <file.docx>\n  outline  --in <file.docx> [--out <file.json>]\n  find     --in <file.docx> --query <text|regex> [--regex true|false] [--ignoreCase true|false] [--max N] [--out <file.json>]\n  extract  --in <file.docx> --anchor <anchor.json> [--before N] [--after N] [--out <file.json>]\n  inspect  --in <file.docx> [--out <file.json>]   (full dump; avoid for huge docs)\n  redline  --original <a.docx> --edited <b.docx> --out <tracked.docx> [--author \"AI helper\"]\n  comments list --in <file.docx> [--out <file.json>]\n\nNotes:\n- find searches on normalized paragraph text (concatenated across runs; formatting boundaries ignored).\n- redline uses OpenXmlPowerTools WmlComparer to produce Word tracked-change markup.\n");
	}

	private static int Fail(string msg)
	{
		Console.Error.WriteLine(msg);
		return 1;
	}

	private static string? GetArg(string[] args, string name)
	{
		for (int i = 0; i < args.Length - 1; i++)
		{
			if (args[i] == name)
			{
				return args[i + 1];
			}
		}
		return null;
	}

	private static int GetIntArg(string[] args, string name, int def)
	{
		int result = default(int);
		if (!int.TryParse(GetArg(args, name), ref result))
		{
			return def;
		}
		return result;
	}

	private static bool GetBoolArg(string[] args, string name, bool def)
	{
		string arg = GetArg(args, name);
		if (arg != null)
		{
			if (!arg.Equals("true", (StringComparison)5))
			{
				return arg == "1";
			}
			return true;
		}
		return def;
	}

	private static void WriteJson(object obj, string? outPath)
	{
		//IL_0000: Unknown result type (might be due to invalid IL or missing references)
		//IL_0005: Unknown result type (might be due to invalid IL or missing references)
		//IL_000c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0014: Expected O, but got Unknown
		JsonSerializerOptions val = new JsonSerializerOptions
		{
			WriteIndented = true,
			DefaultIgnoreCondition = (JsonIgnoreCondition)3
		};
		string text = JsonSerializer.Serialize<object>(obj, val);
		if (!string.IsNullOrWhiteSpace(outPath))
		{
			File.WriteAllText(outPath, text, Encoding.UTF8);
		}
		else
		{
			Console.WriteLine(text);
		}
	}

	private static int CmdStatus(string[] args)
	{
		//IL_0031: Unknown result type (might be due to invalid IL or missing references)
		//IL_0053: Unknown result type (might be due to invalid IL or missing references)
		string arg = GetArg(args, "--in");
		if (arg == null)
		{
			return Fail("Missing --in <file.docx>");
		}
		using WordprocessingDocument wordprocessingDocument = WordprocessingDocument.Open(arg, isEditable: false);
		MainDocumentPart mainDocumentPart = wordprocessingDocument.MainDocumentPart ?? throw new InvalidOperationException("Missing MainDocumentPart");
		Body body = mainDocumentPart.Document?.Body ?? throw new InvalidOperationException("Missing Body");
		bool hasTrackedChanges = Enumerable.Any<OpenXmlElement>(body.Descendants(), (Func<OpenXmlElement, bool>)delegate(OpenXmlElement e)
		{
			string localName = e.LocalName;
			return (localName == "ins" || localName == "del" || localName == "moveFrom" || localName == "moveTo" || localName == "moveFromRangeStart" || localName == "moveToRangeStart") ? true : false;
		});
		WordprocessingCommentsPart? wordprocessingCommentsPart = mainDocumentPart.WordprocessingCommentsPart;
		int num;
		if (wordprocessingCommentsPart == null)
		{
			num = 0;
		}
		else
		{
			Comments? comments = wordprocessingCommentsPart.Comments;
			num = ((((comments != null) ? new bool?(Enumerable.Any<Comment>(comments.Elements<Comment>())) : ((bool?)null)) == true) ? 1 : 0);
		}
		bool flag = (byte)num != 0;
		string commentModel = "unknown";
		if (flag)
		{
			commentModel = (Enumerable.Any<string>(Enumerable.Select<IdPartPair, string>(mainDocumentPart.Parts, (Func<IdPartPair, string>)((IdPartPair p) => p.OpenXmlPart.RelationshipType ?? "")), (Func<string, bool>)((string t) => t.Contains("commentsExtended", (StringComparison)5))) ? "modern" : "legacy");
		}
		int paragraphs = Enumerable.Count<Paragraph>(body.Descendants<Paragraph>());
		int headings = Enumerable.Count<Paragraph>(body.Descendants<Paragraph>(), (Func<Paragraph, bool>)((Paragraph p) => GetHeadingLevel(p) > 0));
		WriteJson(new StatusOut(hasTrackedChanges, flag, commentModel, new LengthOut(paragraphs, headings)), null);
		return 0;
	}

	private static int CmdOutline(string[] args)
	{
		string arg = GetArg(args, "--in");
		if (arg == null)
		{
			return Fail("Missing --in <file.docx>");
		}
		string arg2 = GetArg(args, "--out");
		using WordprocessingDocument wordprocessingDocument = WordprocessingDocument.Open(arg, isEditable: false);
		List<Paragraph> val = Enumerable.ToList<Paragraph>(wordprocessingDocument.MainDocumentPart.Document.Body.Descendants<Paragraph>());
		List<OutlineItem> val2 = new List<OutlineItem>();
		for (int i = 0; i < val.Count; i++)
		{
			Paragraph p = val[i];
			int headingLevel = GetHeadingLevel(p);
			if (headingLevel > 0)
			{
				string paraId = GetParaId(p, i);
				string text = NormalizeParaText(p, "visible");
				if (text.Length > 300)
				{
					text = text.Substring(0, 300) + "…";
				}
				val2.Add(new OutlineItem(i, paraId, headingLevel, text));
			}
		}
		WriteJson(new
		{
			outline = val2
		}, arg2);
		return 0;
	}

	private static int GetHeadingLevel(Paragraph p)
	{
		string text = p.ParagraphProperties?.ParagraphStyleId?.Val?.Value;
		if (string.IsNullOrWhiteSpace(text))
		{
			return 0;
		}
		Match val = Regex.Match(text, "Heading\\s*([1-9])", (RegexOptions)1);
		if (((Group)val).Success)
		{
			return int.Parse(((Capture)val.Groups[1]).Value);
		}
		val = Regex.Match(text, "Heading([1-9])", (RegexOptions)1);
		if (((Group)val).Success)
		{
			return int.Parse(((Capture)val.Groups[1]).Value);
		}
		return 0;
	}

	private static string GetParaId(Paragraph p, int idx)
	{
		string value = p.GetAttribute("paraId", "http://schemas.microsoft.com/office/word/2010/wordml").Value;
		if (!string.IsNullOrWhiteSpace(value))
		{
			return value;
		}
		return $"p{idx:000000}";
	}

	private static string NormalizeParaText(Paragraph p, string mode)
	{
		//IL_0000: Unknown result type (might be due to invalid IL or missing references)
		//IL_0006: Expected O, but got Unknown
		StringBuilder val = new StringBuilder();
		global::System.Collections.Generic.IEnumerator<OpenXmlElement> enumerator = p.Descendants().GetEnumerator();
		try
		{
			while (((global::System.Collections.IEnumerator)enumerator).MoveNext())
			{
				OpenXmlElement current = enumerator.Current;
				if (current is Text text)
				{
					if (ShouldIncludeNode(current, mode))
					{
						val.Append(text.Text);
					}
				}
				else if (current is DeletedText deletedText)
				{
					if (ShouldIncludeDeleted(current, mode))
					{
						val.Append(deletedText.Text);
					}
				}
				else if (current is TabChar)
				{
					if (ShouldIncludeNode(current, mode))
					{
						val.Append('\t');
					}
				}
				else if (current is Break && ShouldIncludeNode(current, mode))
				{
					val.Append('\n');
				}
			}
		}
		finally
		{
			((global::System.IDisposable)enumerator)?.Dispose();
		}
		return ((object)val).ToString();
	}

	private static bool ShouldIncludeNode(OpenXmlElement node, string mode)
	{
		if (mode.Equals("all", (StringComparison)5))
		{
			return true;
		}
		bool flag = Enumerable.Any<OpenXmlElement>(node.Ancestors(), (Func<OpenXmlElement, bool>)delegate(OpenXmlElement a)
		{
			string localName = a.LocalName;
			return (localName == "del" || localName == "moveFrom") ? true : false;
		});
		bool flag2 = Enumerable.Any<OpenXmlElement>(node.Ancestors(), (Func<OpenXmlElement, bool>)delegate(OpenXmlElement a)
		{
			string localName = a.LocalName;
			return (localName == "ins" || localName == "moveTo") ? true : false;
		});
		if (mode.Equals("visible", (StringComparison)5))
		{
			return !flag;
		}
		if (mode.Equals("original", (StringComparison)5))
		{
			return !flag2;
		}
		return true;
	}

	private static bool ShouldIncludeDeleted(OpenXmlElement node, string mode)
	{
		if (mode.Equals("all", (StringComparison)5))
		{
			return true;
		}
		bool flag = Enumerable.Any<OpenXmlElement>(node.Ancestors(), (Func<OpenXmlElement, bool>)delegate(OpenXmlElement a)
		{
			string localName = a.LocalName;
			return (localName == "del" || localName == "moveFrom") ? true : false;
		});
		bool flag2 = Enumerable.Any<OpenXmlElement>(node.Ancestors(), (Func<OpenXmlElement, bool>)delegate(OpenXmlElement a)
		{
			string localName = a.LocalName;
			return (localName == "ins" || localName == "moveTo") ? true : false;
		});
		if (mode.Equals("visible", (StringComparison)5))
		{
			return false;
		}
		if (mode.Equals("original", (StringComparison)5))
		{
			if (flag)
			{
				return !flag2;
			}
			return false;
		}
		return false;
	}

	private static int CmdFind(string[] args)
	{
		//IL_008f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0092: Unknown result type (might be due to invalid IL or missing references)
		//IL_0094: Unknown result type (might be due to invalid IL or missing references)
		//IL_009b: Expected O, but got Unknown
		//IL_0181: Unknown result type (might be due to invalid IL or missing references)
		//IL_0115: Unknown result type (might be due to invalid IL or missing references)
		//IL_011c: Expected O, but got Unknown
		//IL_018d: Unknown result type (might be due to invalid IL or missing references)
		string arg = GetArg(args, "--in");
		if (arg == null)
		{
			return Fail("Missing --in <file.docx>");
		}
		string arg2 = GetArg(args, "--query");
		if (arg2 == null)
		{
			return Fail("Missing --query <text|regex>");
		}
		string arg3 = GetArg(args, "--out");
		int intArg = GetIntArg(args, "--max", 50);
		bool boolArg = GetBoolArg(args, "--regex", def: false);
		bool boolArg2 = GetBoolArg(args, "--ignoreCase", def: true);
		string mode = GetArg(args, "--mode") ?? "visible";
		Regex val = null;
		if (boolArg)
		{
			RegexOptions val2 = (RegexOptions)(boolArg2 ? 1 : 0);
			val = new Regex(arg2, val2);
		}
		using (WordprocessingDocument wordprocessingDocument = WordprocessingDocument.Open(arg, isEditable: false))
		{
			List<Paragraph> val3 = Enumerable.ToList<Paragraph>(wordprocessingDocument.MainDocumentPart.Document.Body.Descendants<Paragraph>());
			List<FindHit> val4 = new List<FindHit>();
			for (int i = 0; i < val3.Count; i++)
			{
				if (val4.Count >= intArg)
				{
					break;
				}
				Paragraph p = val3[i];
				string paraId = GetParaId(p, i);
				string text = NormalizeParaText(p, mode);
				if (string.IsNullOrEmpty(text))
				{
					continue;
				}
				if (boolArg)
				{
					foreach (Match item in val.Matches(text))
					{
						Match val5 = item;
						if (((Group)val5).Success)
						{
							val4.Add(MkHit(i, paraId, text, ((Capture)val5).Index, ((Capture)val5).Index + ((Capture)val5).Length));
							if (val4.Count >= intArg)
							{
								break;
							}
						}
					}
					continue;
				}
				StringComparison val6 = (StringComparison)(boolArg2 ? 5 : 4);
				int num = 0;
				while (val4.Count < intArg)
				{
					int num2 = text.IndexOf(arg2, num, val6);
					if (num2 < 0)
					{
						break;
					}
					val4.Add(MkHit(i, paraId, text, num2, num2 + arg2.Length));
					num = num2 + Math.Max(1, arg2.Length);
				}
			}
			WriteJson(new
			{
				query = arg2,
				isRegex = boolArg,
				ignoreCase = boolArg2,
				mode = mode,
				hits = val4
			}, arg3);
			return 0;
		}
		[CompilerGenerated]
		static FindHit MkHit(int index, string id, string text2, int start, int end)
		{
			int num3 = Math.Max(0, start - 40);
			int num4 = Math.Min(text2.Length, end + 40);
			string context = text2.Substring(num3, num4 - num3);
			string match = text2.Substring(start, end - start);
			return new FindHit(index, id, start, end, match, context);
		}
	}

	private static int CmdExtract(string[] args)
	{
		//IL_008b: Unknown result type (might be due to invalid IL or missing references)
		string arg = GetArg(args, "--in");
		if (arg == null)
		{
			return Fail("Missing --in <file.docx>");
		}
		string arg2 = GetArg(args, "--anchor");
		if (arg2 == null)
		{
			return Fail("Missing --anchor <anchor.json>");
		}
		string arg3 = GetArg(args, "--out");
		int intArg = GetIntArg(args, "--before", 2);
		int intArg2 = GetIntArg(args, "--after", 2);
		string mode = GetArg(args, "--mode") ?? "visible";
		Anchor anchor = JsonSerializer.Deserialize<Anchor>(File.ReadAllText(arg2, Encoding.UTF8), (JsonSerializerOptions)null) ?? throw new InvalidOperationException("Invalid anchor.json");
		using WordprocessingDocument wordprocessingDocument = WordprocessingDocument.Open(arg, isEditable: false);
		List<Paragraph> val = Enumerable.ToList<Paragraph>(wordprocessingDocument.MainDocumentPart.Document.Body.Descendants<Paragraph>());
		int num = -1;
		for (int i = 0; i < val.Count; i++)
		{
			if (GetParaId(val[i], i) == anchor.paraId)
			{
				num = i;
				break;
			}
		}
		if (num < 0)
		{
			return Fail("paraId not found: " + anchor.paraId);
		}
		int num2 = Math.Max(0, num - intArg);
		int num3 = Math.Min(val.Count - 1, num + intArg2);
		List<object> val2 = new List<object>();
		for (int j = num2; j <= num3; j++)
		{
			Paragraph p = val[j];
			val2.Add((object)new
			{
				index = j,
				paraId = GetParaId(p, j),
				text = NormalizeParaText(p, mode),
				isTarget = (j == num)
			});
		}
		WriteJson(new
		{
			anchor = anchor,
			window = new
			{
				from = num2,
				to = num3,
				before = intArg,
				after = intArg2
			},
			paragraphs = val2
		}, arg3);
		return 0;
	}

	private static int CmdInspect(string[] args)
	{
		string arg = GetArg(args, "--in");
		if (arg == null)
		{
			return Fail("Missing --in <file.docx>");
		}
		string arg2 = GetArg(args, "--out");
		string mode = GetArg(args, "--mode") ?? "visible";
		using WordprocessingDocument wordprocessingDocument = WordprocessingDocument.Open(arg, isEditable: false);
		var paragraphs = Enumerable.ToList(Enumerable.Select((global::System.Collections.Generic.IEnumerable<Paragraph>)Enumerable.ToList<Paragraph>(wordprocessingDocument.MainDocumentPart.Document.Body.Descendants<Paragraph>()), (Paragraph p, int i) => new
		{
			index = i,
			paraId = GetParaId(p, i),
			headingLevel = GetHeadingLevel(p),
			text = NormalizeParaText(p, mode)
		}));
		WriteJson(new { mode, paragraphs }, arg2);
		return 0;
	}

	private static int CmdRedline(string[] args)
	{
		string arg = GetArg(args, "--original");
		if (arg == null)
		{
			return Fail("Missing --original <a.docx>");
		}
		string arg2 = GetArg(args, "--edited");
		if (arg2 == null)
		{
			return Fail("Missing --edited <b.docx>");
		}
		string arg3 = GetArg(args, "--out");
		if (arg3 == null)
		{
			return Fail("Missing --out <tracked.docx>");
		}
		string authorForRevisions = GetArg(args, "--author") ?? "AI helper";
		WmlDocument source = new WmlDocument(arg);
		WmlDocument source2 = new WmlDocument(arg2);
		WmlComparerSettings settings = new WmlComparerSettings
		{
			AuthorForRevisions = authorForRevisions
		};
		WmlComparer.Compare(source, source2, settings).SaveAs(arg3);
		return 0;
	}

	private static int CmdComments(string[] args)
	{
		if (args.Length == 0)
		{
			return Fail("Missing comments subcommand (list)");
		}
		string text = args[0];
		string[] args2 = Enumerable.ToArray<string>(Enumerable.Skip<string>((global::System.Collections.Generic.IEnumerable<string>)args, 1));
		if (text == "list")
		{
			return CmdCommentsList(args2);
		}
		return Fail("Unknown comments subcommand: " + text + " (only list implemented in v0.1)");
	}

	private static int CmdCommentsList(string[] args)
	{
		//IL_003d: Unknown result type (might be due to invalid IL or missing references)
		string arg = GetArg(args, "--in");
		if (arg == null)
		{
			return Fail("Missing --in <file.docx>");
		}
		string arg2 = GetArg(args, "--out");
		using WordprocessingDocument wordprocessingDocument = WordprocessingDocument.Open(arg, isEditable: false);
		WordprocessingCommentsPart wordprocessingCommentsPart = (wordprocessingDocument.MainDocumentPart ?? throw new InvalidOperationException("Missing MainDocumentPart")).WordprocessingCommentsPart;
		if (wordprocessingCommentsPart?.Comments == null)
		{
			WriteJson(new
			{
				comments = global::System.Array.Empty<CommentOut>()
			}, arg2);
			return 0;
		}
		WriteJson(new
		{
			comments = Enumerable.ToList<CommentOut>(Enumerable.Select<Comment, CommentOut>(wordprocessingCommentsPart.Comments.Elements<Comment>(), (Func<Comment, CommentOut>)delegate(Comment c)
			{
				string? id = c.Id?.Value ?? "";
				string author = c.Author?.Value;
				string initials = c.Initials?.Value;
				string date = c.Date?.Value.ToString("o");
				string text = string.Join("", Enumerable.Select<Text, string>(c.Descendants<Text>(), (Func<Text, string>)((Text t) => t.Text)));
				return new CommentOut(id, author, initials, date, text);
			}))
		}, arg2);
		return 0;
	}
}
